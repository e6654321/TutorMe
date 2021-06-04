from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Schedule, Subject, Mentor, Mentee, Details, Account, Notes, Receipt
from .forms import CreateUserForm, CreateProfileForm, CardDetailsForm, AccountForm, CreateSubjectForm, ReceiptForm, CreateMenteeForm, CreateMentorForm
from django.db.models import Q
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

from .modelsFolder.AdminModel import AdminModel
from .modelsFolder.ScheduleModel import ScheduleModel
from .templatesFolder.AdminTemplate import AdminTemplate
from .templatesFolder.CommonUserTemplate import CommonUserTemplate

class HomePageView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'search.html')
        return render(request, 'index.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pages:search')
        else:
            messages.info(request, "Username or password incorrect")
            return render(request, 'index.html')


class RegisterView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'search.html')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = request.POST.copy()
        form = AdminModel.addUser(form)
        if form:
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created ' + username)
            return redirect('pages:login')
        else:
            messages.error(request, 'Check inputs and try again')
            print(form.errors)

        context = {'form': form}
        return render(request, 'register.html', context)


class logoutUser(TemplateView):
    def get(self, request):
        return AdminTemplate.logout(self, request)

class MainView(TemplateView):
    template_name = 'main.html'

class RequestSchedView(TemplateView):
    def get(self, request):
        return AdminTemplate.viewSchedule(self, request)

    def post(self, request):
        if request.method == 'POST':
            subjectID = request.POST.get("subjectID")
            mode = 'E-Wallet'

            if 'com' in request.POST:
                mode = 'Cash on Delivery'
            elif 'card-btn' in request.POST:
                mode = 'Credit Card'
            subject = Subject.objects.filter(id=subjectID)
            date = subject.values('session_date')[0].get('session_date')
            ratePrHour = subject.values('ratePerHour')[0].get('ratePerHour')
            time = (subject.values('session_time_start')[0].get('session_time_start'))+ " - " +(subject.values('session_time_end')[0].get('session_time_end'))
            print(time)
            custom_time_start = request.POST.get("timepicker")
            custom_time_end = request.POST.get("timepicker1")

            form = Schedule(subject=subject[0],menteeID=request.user,date=date,ratePrHour=ratePrHour, time=time, custom_time_start=custom_time_start,
                            custom_time_end=custom_time_end, payment_method=mode)
            form.save()

            return redirect('pages:search')
        else:
            return HttpResponse('failed')


class NotesPageView(TemplateView):
    # template_name='notes.html'
    def get(self, request):
        return CommonUserTemplate.viewNotes(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
                print(sort)
                if sort == 'subjectName':
                    sort = 'subjectID__subjectName'
                if sort == 'ratePerHour':
                    sort = 'subjectID__ratePerHour'
                if sort == '-subjectName':
                    sort = '-subjectID__subjectName'
                if sort == '-ratePerHour':
                    sort = '-subjectID__ratePerHour'
        n = Notes.objects.all()
        n = n.filter(Q(subjectID__subjectName__icontains=item) | Q(mentorID__first_name__icontains=item)
                     | Q(mentorID__last_name__icontains=item)).values('subjectID__subjectName',
                                                                     'mentorID__first_name', 'mentorID__last_name', 'subjectID__ratePerHour', 'notes', 'notesTitle').order_by(sort)
        data = {
            "notes": n
        }
        return render(request, 'notes.html', data)


class SearchView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.search(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
                userId = request.user.id
                queries = [((Q(id=sched.subject.id)) if userId == sched.menteeID.id else (Q(id=0))) for sched in Schedule.objects.all()]
                s1 = Subject.objects.filter(Q(subjectName__icontains=item) | Q(mentorID__first_name__icontains=item)
                                        | Q(mentorID__last_name__icontains=item))
                print(s1)
                try:
                    query = queries.pop()
                    for item in queries:
                        query |= item
                    print(query)
                    s2 =s1.filter(~query).distinct()
                except IndexError as e:
                    s2 = s1.filter()
                print(s2)
                data = {
                    "subject": s2.values('id','subjectName', 'ratePerHour',
                                            'session_date', 'session_time_start', 'session_time_end',
                                            'mentorID__first_name', 'mentorID__last_name').order_by(sort)
                }
                return render(request, 'search.html', data)


class GeolocationView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.geolocation(self, request)


class ProfileView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.viewProfile(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnUpdate' in request.POST:
                AdminModel.updateUser(request)
                return render(request, 'profile.html', {
                    "user": user[0],
                    "profile": profile[0],
                })
            elif 'cancelUpdate' in request.POST:
                return redirect('pages:profile')


class PaymentView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.viewPayment(self, request)

    def post(self, request):
        if request.method == 'POST':
            print(request.POST)
            if 'btnUpdateCard' in request.POST:
                print("Update detail button clicked!")
                did = request.POST.get('did')
                print(did)
                cardOwnerName = request.POST.get('cardOwnerName')
                cardNum = request.POST.get('cardNum')
                month = request.POST.get('month')
                year = request.POST.get('year')
                cvc = request.POST.get('cvc')
                if (did):
                    Details.objects.filter(id=did).update(cardOwnerName=cardOwnerName,cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                    
                    s1 = Account.objects.filter(userID=request.user)
                    details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                        'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                    print(details)
                    data = {
                        "details": details
                    }
                    return render(request, 'payment.html', data)
                else:
                    details = Details(cardOwnerName=cardOwnerName,cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                    details.save()
                    print(details.id)

                    Account.objects.filter(userID=request.user).update(detailID=details)
                    s1 = Account.objects.filter(userID=request.user)
                    details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                        'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                    print(details)
                    data = {
                        "details": [details]
                    }
                    return render(request, 'payment.html', data)
            elif 'btnDeleteCard' in request.POST:
                print("Delete product button clicked!")
                did = request.POST.get('did')
                rid = request.POST.get('rid')
                aid = request.POST.get('aid')
                if (did):
                    details = Details.objects.filter(pk = did).delete()
                    print(details)
                if (rid):
                    receipt = Receipt.objects.filter(pk = rid).delete()
                    print(receipt)
                if (aid):
                    acc = Account.objects.filter(pk = aid).delete()
                    print(acc)
                print("Record deleted!")
                return redirect('pages:addpayment')


class AddPaymentView(TemplateView):
    def get(self, request):
        return render(request, 'addpayment.html')

    def post(self, request):
        current_user = request.user
        cardOwnerName = request.POST.get('cardOwnerName')
        cardNum = request.POST.get('cardNumber')
        month = request.POST.get('expire_month')
        year = request.POST.get('expire_year')
        cvc= request.POST.get('cvc')
        # form = Details(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
        #                 expire_month=month, expire_year=year, cvc=cvc)
        accForm = Account(userID=current_user)
        print(cvc)
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            accForm.save()

            saved_details = Details.objects.filter(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
                        expire_month=month, expire_year=year, cvc=cvc)
            print(saved_details)
            Account.objects.filter(userID=current_user).update(detailID=saved_details[0])
            s1 = Account.objects.filter(userID=current_user)
            details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
            print(details)
            data = {
                "details": [details]
            }
            return render(request, 'payment.html', data)
        else:
            messages.error(request, 'Check inputs and try again')
            return render(request, 'addpayment.html')


class SettingsView(TemplateView):
    template_name = CommonUserTemplate.viewSettings('')


class MessagingView(TemplateView):
    template_name = 'messaging.html'


class CreateSubjectView(TemplateView):
    # template_name= 'create-subject.html'
    def get(self, request):
        return ScheduleModel.addSched(self, request)

    def post(self, request):
        form = CreateSubjectForm(request.POST)
        print(form.errors)
        mentors = ''
        if request.user.is_authenticated:
            current_user = request.user

        if form.is_valid:
            subName = request.POST.get('subjectName')
            subDate = request.POST.get('session_date')
            timeStart = request.POST.get('session_time_start')
            timeEnd = request.POST.get('session_time_end')
            rate = request.POST.get('ratePerHour')
            category = request.POST.get('category')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print(latitude,longitude)
            form = Subject(subjectName=subName,  session_date=subDate,
                           session_time_start=timeStart, session_time_end=timeEnd,
                           ratePerHour=rate, category=category, mentorID=current_user,
                           latitude=latitude, longitude=longitude
                           )
            print(form.mentorID)
            form.save()
            return redirect('pages:search')
        else:
            messages.error(request, 'Check inputs and try again')
            print(form.errors)
            return render(request, 'create-subject.html')


class ScheduleSubjectView(TemplateView):
    template_name = 'schedule-page.html'


class MentorProfileView(TemplateView):
    template_name = 'mentor-profile.html'


class ChatBotView(TemplateView):
    template_name = 'Chatbot.html'

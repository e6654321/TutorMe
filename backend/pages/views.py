from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Profile, Schedule, Subject, Mentor, Details, Account, Notes, Receipt
from .forms import CreateUserForm, CardDetailsForm, AccountForm, CreateSubjectForm, ReceiptForm
from django.db.models import Q
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder


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
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created ' + user)
            context = {'form': form}
            return redirect('pages:login')
        else:
            messages.error(request, 'Check inputs and try again')
            print(form.errors)

        context = {'form': form}
        return render(request, 'register.html', context)


class logoutUser(TemplateView):
    def get(self, request):
        logout(request)
        return redirect('pages:addpayment')


class MainView(TemplateView):
    template_name = 'main.html'


class RequestSchedView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            sub = Subject.objects.filter(mentorID=1).values('mentorID', 'subjectName', 'ratePerHour',
                                                            'session_date', 'session_time_end', 'session_time_start', 'category', 'mentorID__firstName', 'mentorID__lastName')

            print(current_user)
            subject = {
                'subject': sub
            }
            return render(request, 'RequestSched.html', subject)

    def post(self, request):
        if request.method == 'POST':
            subject = Subject.objects.filter(mentorID=1)
            #menteeID = Mentee.objects.filter(menteeID=3)
            date = request.POST.get("datepicker")
            time = request.POST.get("time")
            custom_time_start = request.POST.get("timepicker")
            custom_time_end = request.POST.get("timepicker1")
            payment_method = "DUNNO"
            # if "ewallet" in request.POST:
            #     payment_method = "E-Wallet"
            # if "com" in request.POST:
            #     payment_method = "Cash On Meet-up"
            # if "credit" in request.POST:
            #     payment_method = "Credit"
            form = Schedule(date=date, time=time, custom_time_start=custom_time_start,
                            custom_time_end=custom_time_end, payment_method=payment_method)
            form.save()

            return render(request, 'RequestSched.html')
        else:
            return HttpResponse('failed')


class NotesPageView(TemplateView):
    # template_name='notes.html'
    def get(self, request):
        if request.user.is_authenticated:
            n = Notes.objects.all().values('menteeID', 'mentorID', 'subjectID', 'notes',
                                           'notesTitle', 'subjectID__subjectName')
            data = {
                "notes": n
            }
            return render(request, 'notes.html', data)

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
        n = n.filter(Q(subjectID__subjectName__icontains=item) | Q(mentorID__firstName__icontains=item)
                     | Q(mentorID__lastName__icontains=item)).values('subjectID__subjectName',
                                                                     'mentorID__firstName', 'mentorID__lastName', 'subjectID__ratePerHour', 'notes', 'notesTitle').order_by(sort)
        data = {
            "notes": n
        }
        return render(request, 'notes.html', data)


class SearchView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            s1 = Subject.objects.all().values('subjectName', 'ratePerHour',
                                              'session_date', 'session_time_start',
                                              'mentorID__firstName', 'mentorID__lastName')
            data = {
                "subject": s1
            }
            return render(request, 'search.html', data)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
        s1 = Subject.objects.filter(Q(subjectName__icontains=item) | Q(mentorID__firstName__icontains=item)
                                    | Q(mentorID__lastName__icontains=item)).values('subjectName', 'ratePerHour',
                                                                                    'session_date', 'session_time_start',
                                                                                    'mentorID__firstName', 'mentorID__lastName').order_by(sort)
        data = {
            "subject": s1
        }
        return render(request, 'search.html', data)


class GeolocationView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            json_serializer = serializers.get_serializer("json")()
            scheds = json_serializer.serialize(
                Schedule.objects.all().order_by('id'))
            mentors = json_serializer.serialize(
                Mentor.objects.all().order_by('id'))
            subjects = json_serializer.serialize(
                Subject.objects.all().order_by('id'))
            profiles = json.dumps(list(Mentor.objects.all().values(
                'id', 'firstName', 'lastName')), cls=DjangoJSONEncoder)
            data = {
                "scheds": scheds,
                "mentors": mentors,
                "subjects": subjects,
                "profiles": profiles,
            }
            return render(request, 'geolocation.html', data)


class ProfileView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            print(current_user)
            for attr in dir(current_user):
                try:
                    print('%s: %s' % (attr, getattr(current_user, attr)))
                except Exception as e:
                    print('%s: %s' % (attr, e))
            return render(request, 'profile.html', {"user": current_user})
            # else:
            #     return redirect('pages:addpayment')


class PaymentView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            print("user")
            print(current_user.id)
            acc = Account.objects.filter(userID=request.user)
            if acc.exists():
                s1 = Account.objects.filter(userID=request.user).value('detailID__cardOwnerName', 'detailID__cardNumber', 
                'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                data = {
                    "details": s1
                }
                return render(request, 'payment.html', data)
            else:
                return redirect('pages:addpayment')

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
                update_details = Details.objects.filter(id=did).update(cardOwnerName=cardOwnerName,
                                                                       cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                print(update_details)
                print("Details updated!")
                return redirect('pages:payment')
            elif 'btnDeleteCard' in request.POST:
                print("Delete product button clicked!")
                did = request.POST.get('did')
                rid = request.POST.get('rid')
                aid = request.POST.get('aid')
                details = Details.objects.filter(pk = did).delete()
                receipt = Receipt.objects.filter(pk = rid).delete()
                acc = Account.objects.filter(pk = aid).delete()
                print(details)
                print(receipt)
                print(acc)
                print("Record deleted!")
                return redirect('pages:addpayment')


class AddPaymentView(TemplateView):
    def get(self, request):
        return render(request, 'addpayment.html')

    def post(self, request):
        form = CardDetailsForm(request.POST)
        # receiptForm = ReceiptForm(request.POST)
        print("error") 
        print(form.errors)
        # print(receiptForm.errors)
        current_user = request.user

        if form.is_valid():
            cardOwnerName = request.POST.get('cardOwnerName')
            cardNum = request.POST.get('cardNum')
            month = request.POST.get('month')
            year = request.POST.get('year')
            cvc= request.POST.get('cvc')
            form = Details(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
                            expire_month=month, expire_year=year, cvc=cvc)
            accForm = Account(userID=request.user, detailID=form.id, receiptID=None)
            card = form.save()
            accForm.save()

            return redirect('pages:payment')
        else:
            messages.error(request, 'Check inputs and try again')
            return render(request, 'addpayment.html')


class SettingsView(TemplateView):
    template_name = 'settings.html'


class MessagingView(TemplateView):
    template_name = 'messaging.html'


class CreateSubjectView(TemplateView):
    # template_name= 'create-subject.html'
    def get(self, request):
        mentors = Mentor.objects.all()
        try:
            mentors = Mentor.objects.get(user_id=request.user.id)
            return render(request, 'create-subject.html')
        except:
            messages.error(
                request, 'You are not a mentor. You will be redirected momentarily.')
            return render(request, 'create-subject.html')

    def post(self, request):
        form = CreateSubjectForm(request.POST)
        print(form.errors)
        mentors = ''
        if request.user.is_authenticated:
            current_user = request.user
            mentors = Mentor.objects.get(user_id=current_user.id)

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
                           ratePerHour=rate, category=category, mentorID=mentors,
                           latitude=latitude, longitude=longitude
                           )
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

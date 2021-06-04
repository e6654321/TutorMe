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
        form = CreateUserForm(form)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            if (form.cleaned_data['is_staff']):
                user.first_name = 'Jhosie'
                user.last_name = 'Espantaleon'
            else:
                user.first_name = 'Elram'
                user.last_name = 'Espra'
            user.save()
            print(user)
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created ' + username)
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
            schedId = request.GET.get('id')
            print(schedId)
            sub = Subject.objects.filter(id=schedId).values('id','mentorID', 'subjectName', 'ratePerHour',
                                                            'session_date', 'session_time_end', 'session_time_start', 'category', 'mentorID__first_name', 'mentorID__last_name')

            profile = Profile.objects.filter(user_id=request.user.id)
            account = Account.objects.filter(userID_id=request.user.id)
            cardId = account.values('detailID_id')[0].get('detailID_id')
            card = Details.objects.filter(id=cardId)
            subject = {
                'subject': sub,
                'profile': profile[0],
                'card': card[0]
            }
            return render(request, 'RequestSched.html', subject)

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
        n = n.filter(Q(subjectID__subjectName__icontains=item) | Q(mentorID__first_name__icontains=item)
                     | Q(mentorID__last_name__icontains=item)).values('subjectID__subjectName',
                                                                     'mentorID__first_name', 'mentorID__last_name', 'subjectID__ratePerHour', 'notes', 'notesTitle').order_by(sort)
        data = {
            "notes": n
        }
        return render(request, 'notes.html', data)


class SearchView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            userId = request.user.id
            queries = [((Q(id=sched.subject.id)) if userId == sched.menteeID.id else (Q(id=0))) for sched in Schedule.objects.all()]
            
            try:
                query = queries.pop()
                for item in queries:
                    query |= item
                print(query)
                s1 = Subject.objects.exclude(query).values('id','subjectName', 'ratePerHour',
                                        'session_date', 'session_time_start', 'session_time_end',
                                        'mentorID__first_name', 'mentorID__last_name')
            except IndexError as e:
                s1 = Subject.objects.all().values('id','subjectName', 'ratePerHour',
                                        'session_date', 'session_time_start', 'session_time_end',
                                        'mentorID__first_name', 'mentorID__last_name')
            data = {
                "subject": s1
            }
            return render(request, 'search.html', data)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
        s1 = Subject.objects.filter(Q(subjectName__icontains=item) | Q(mentorID__first_name__icontains=item)
                                    | Q(mentorID__last_name__icontains=item)).values('subjectName', 'ratePerHour',
                                                                                    'session_date', 'session_time_start',
                                                                                    'mentorID__first_name', 'mentorID__last_name').order_by(sort)
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
            mentor = json_serializer.serialize(
                User.objects.all().order_by('id'))
            subjects = json_serializer.serialize(
                Subject.objects.all().order_by('id'))
            data = {
                "scheds": scheds,
                "mentor": mentor,
                "subjects": subjects,
            }
            return render(request, 'geolocation.html', data)


class ProfileView(TemplateView):
    def get(self, request):
        current_user = request.user
        user = User.objects.filter(id=current_user.id)
        profile = Profile.objects.filter(user=current_user)
        user[0].refresh_from_db()
        if(profile):
            return render(request, 'profile.html', {
                "user": user[0],
                "profile": profile[0],
            })
        else:
            profile = {}
            print("blank profile")
            print(profile)

            return render(request, 'profile.html', {
                    "user": user[0],
                    "profile": profile,
            })

    def post(self, request):
        if request.method == 'POST':
            if 'btnUpdate' in request.POST:
                fname = request.POST.get('fname')
                mname = request.POST.get('mname')
                lname = request.POST.get('lname')
                email = request.POST.get('email')
                number = request.POST.get('number')
                username = request.POST.get('username')
                User.objects.filter(
                        id=request.user.id
                    ).update(first_name=fname,last_name=lname, email=email, username=username)
                
                
                profile = Profile.objects.filter(user=request.user)

                if profile.exists():
                    profile.update(middleName=mname,contactNo=number)
                else:
                    updateProfile = Profile(user=request.user,middleName=mname,contactNo=number)
                    updateProfile.save()
                print('update')

                user = User.objects.filter(id=request.user.id)
                profile = Profile.objects.filter(user=request.user)

                print(profile[0])
                return render(request, 'profile.html', {
                    "user": user[0],
                    "profile": profile[0],
                })
            elif 'cancelUpdate' in request.POST:
                return redirect('pages:profile')


class PaymentView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            print("user")
            acc = Account.objects.filter(userID=current_user)
            print(acc)
            if acc.exists():
                s1 = Account.objects.filter(userID=current_user)
                hasValue = bool(s1.values()[0].get('detailID_id'))
                
                if(hasValue):
                    details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                else:
                    details = [Details()]
                data = {
                    "details": details
                }
                print('get')
                print([details])
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
    template_name = 'settings.html'


class MessagingView(TemplateView):
    template_name = 'messaging.html'


class CreateSubjectView(TemplateView):
    # template_name= 'create-subject.html'
    def get(self, request):
        mentors = Mentor.objects.all()
        try:
            if (request.user.is_staff):
                return render(request, 'create-subject.html')
                
            messages.error(
                request, 'You are not a mentor. You will be redirected momentarily.')
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

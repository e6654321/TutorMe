from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User, Schedule, Subject, Mentor, Details, Account
from .forms import CreateUserForm, CardDetailsForm
from django.db.models import Q

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
        context = {'form':form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account created ' + user)
            context = {'form':form}
            return redirect('pages:login')
        else:
            messages.error(request, 'Check inputs and try again')
            print(form.errors)

        context = {'form':form}
        return render(request, 'register.html', context)

class logoutUser(TemplateView):
    def get(self, request):
        logout(request)
        return render(request, 'index.html')

class MainView(TemplateView):
    template_name = 'main.html'

class RequestSchedView(TemplateView):
	template_name = 'RequestSched.html'

class NotesPageView(TemplateView):
    template_name='notes.html'

class SearchView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            s1 = Subject.objects.all().values('subjectName', 'ratePerHour',
                                        'session_date', 'session_time',
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
                                    'session_date', 'session_time',
                                    'mentorID__firstName', 'mentorID__lastName').order_by(sort)
        data = {
            "subject": s1
        }
        return render(request, 'search.html', data)

    

class GeolocationView(TemplateView):
    template_name = 'geolocation.html'

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
            print(current_user.id)
            acc = Account.objects.filter(userID__id=current_user.id)
            if acc.exists():
                s1 = Account.objects.filter(userID__id=current_user.id).value('detailID__cardOwnerName', 'detailID__cardNumber', 
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
                print("Update product button clicked!")
                did = request.POST.get('id')
                cardOwnerName = request.POST.get('cardOwnerName')
                cvc= request.POST.get('cvc')
                update_details = Details.objects.filter(id = did).update(cardOwnerName=cardOwnerName, 
                                    cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                print(update_details)
                print("Details updated!")
            elif 'btnDeleteCard' in request.POST:
                print("Delete product button clicked!")
                did = request.POST.get("id")
                details = Details.objects.filter(pk = did).delete()
                print(details)
                print("Record deleted!")
        current_user = request.user
        print(current_user.id)
        s1 = Account.objects.filter(userID__id=current_user.id).value('detailID__cardOwnerName', 'detailID__cardNumber', 
        'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
        data = {
            "details": s1
        }
        return redirect('pages:addpayment')

class AddPaymentView(TemplateView):
    def get(self, request):
        return render(request, 'addpayment.html')

    def post(self, request):
        form = CardDetailsForm(request.POST)
        print(form.errors)
        if request.method == 'POST':
            return redirect('pages:search')

        if form.is_valid():
            cardOwnerName = request.POST.get('cardOwnerName')
            cardNum =request.POST.get('cardNum')
            month = request.POST.get('month')
            year = request.POST.get('year')
            cvc= request.POST.get('cvc')
            form = Details(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
                            expire_month=month, expire_year=year, cvc=cvc)
            form.save()
            return redirect('pages:payment')
        else:
            messages.error(request, 'Check inputs and try again')
            return render(request, 'addpayment.html')
        


class SettingsView(TemplateView):
    template_name = 'settings.html'

class MessagingView(TemplateView):
    template_name='messaging.html'

class CreateSubjectView(TemplateView):
    template_name= 'create-subject.html'

class ScheduleSubjectView(TemplateView):
    template_name= 'schedule-page.html'

class MentorProfileView(TemplateView):
    template_name = 'mentor-profile.html'
class ChatBotView(TemplateView):
    template_name = 'Chatbot.html'

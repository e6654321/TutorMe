from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import CreateUserForm

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
    template_name = 'search.html'

class GeolocationView(TemplateView):
    template_name = 'geolocation.html'

class ProfileView(TemplateView):
    template_name = 'profile.html'

class PaymentView(TemplateView):
    template_name = 'payment.html'

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

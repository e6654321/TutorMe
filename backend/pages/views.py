from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index.html'

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

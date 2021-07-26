from django.contrib.auth import login
from django.http import request
from django.urls import path
from django.contrib.auth.decorators import login_required
from pages.views import (
    HomePageView,
    NotesPageView,
    MainView,
    SearchView,
    GeolocationView,
    ProfileView,
    SettingsView,
    PaymentView,
    AddPaymentView,
    MessagingView,
    CreateSubjectView,
    ScheduleSubjectView,
    MentorProfileView,
    RequestSchedView,
    RegisterView,
    logoutUser,
    ChatBotView,
    HistoryView,
    ViewSchedView
)
from pages.viewsFolder.MessageView import MessageView
from . import views

app_name = 'pages'
urlpatterns = [
	path('login/',HomePageView.as_view(),name='login'),
	path('register/',RegisterView.as_view(),name='register'),
	path('RequestSched/',login_required(login_url='pages:login')(RequestSchedView.as_view()), name = 'RequestSched'),
	path('Chatbot/',login_required(login_url='pages:login')(ChatBotView.as_view()), name = 'Chatbot'),
	path('notes/',login_required(login_url='pages:login')(NotesPageView.viewNotes),name='notes'),
	path('addnotes/', login_required(login_url='pages:login')(NotesPageView.createNotes), name='add-notes'),
	path('removeNotes/', login_required(login_url='pages:login')(NotesPageView.removeNote), name='removeNote'),
	path('',login_required(login_url='pages:login')(SearchView.as_view()),name='main'),
	path('search/',login_required(login_url='pages:login')(SearchView.as_view()),name='search'),
	path('geolocation/',login_required(login_url='pages:login')(GeolocationView.as_view()),name='geo'),
	path('profile/',login_required(login_url='pages:login')(ProfileView.as_view()),name='profile'),
	path('settings/',login_required(login_url='pages:login')(SettingsView.as_view()),name='settings'),
	path('payment/',login_required(login_url='pages:login')(PaymentView.as_view()),name='payment'),
	path('addpayment/',login_required(login_url='pages:login')(AddPaymentView.as_view()),name='addpayment'),
	path('messaging/',login_required(login_url='pages:login')(MessageView.as_view()),name='message'),
	path('create-subject/',login_required(login_url='pages:login')(CreateSubjectView.as_view()),name='create-sub'),
	path('schedule/',login_required(login_url='pages:login')(ScheduleSubjectView.as_view()),name='subject-view'),
	path('mentor-profile/',login_required(login_url='pages:login')(MentorProfileView.as_view()),name='mentor-profile'),
	path('logout/',logoutUser.as_view(),name='logout'),
    path('complete/', views.paymentComplete, name="complete"),
    # path('charge/', views.charge, name="charge")
]

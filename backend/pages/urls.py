from django.urls import path
from pages.views import (
	HomePageView,
	NotesPageView, 
	MainView,
	SearchView,
	GeolocationView,
	ProfileView,
	SettingsView,
	PaymentView,
)

app_name = 'pages'
urlpatterns = [
	path('',HomePageView.as_view(),name='login'),
	path('index/',HomePageView.as_view(),name='index'),
	path('notes/',NotesPageView.as_view(),name='notes'),
	path('main/',MainView.as_view(),name='main'),
	path('search/',SearchView.as_view(),name='search'),
	path('geolocation/',GeolocationView.as_view(),name='geo'),
	path('profile/',ProfileView.as_view(),name='profile'),
	path('settings/',SettingsView.as_view(),name='settings'),
	path('payment/',PaymentView.as_view(),name='payment'),


]
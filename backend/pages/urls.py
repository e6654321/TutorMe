from django.urls import path
from .views import (
	HomePageView, 
# 	# DashboardPageView,
# 	# LoginPageView,
# 	# RegCustomerPageView,
# 	# RegProductPageView,
# 	# TableCustomerPageView,
# 	# TableProductPageView,
# 	# TableOrderPageView,
# 	# ErrorPageView
	MainView,
	SearchView,
	GeolocationView,
	ProfileView,
	SettingsView,
	PaymentView
)

app_name = 'pages'
urlpatterns = [
	path('',HomePageView.as_view(),name='login'),
	path('index/',HomePageView.as_view(),name='index'),
	# path('dashboard/',DashboardPageView.as_view(),name='dashboard'),
	# path('login/',LoginPageView.as_view(),name='login'),
	# path('register/customer/',RegCustomerPageView.as_view(),name='regcustomer'),
	# path('register/product/',RegProductPageView.as_view(),name='regproduct'),
	# path('report/customer/',TableCustomerPageView.as_view(),name='tablecustomer'),
	# path('report/product/',TableProductPageView.as_view(),name='tableproduct'),
	# path('report/order/',TableOrderPageView.as_view(),name='tableorder'),
	# path('404/',ErrorPageView.as_view(),name='error'),
	path('main/',MainView.as_view(),name='main'),
	path('search/',SearchView.as_view(),name='search'),
	path('geolocation/',GeolocationView.as_view(),name='geo'),
	path('profile/',ProfileView.as_view(),name='profile'),
	path('settings/',SettingsView.as_view(),name='settings'),
	path('payment/',PaymentView.as_view(),name='payment'),


]
from django.urls import path
from pages.views import (
	HomePageView,
	NotesPageView, 
# 	# DashboardPageView,
# 	# LoginPageView,
# 	# RegCustomerPageView,
# 	# RegProductPageView,
# 	# TableCustomerPageView,
# 	# TableProductPageView,
# 	# TableOrderPageView,
# 	# ErrorPageView
	MainView,
)

app_name = 'pages'
urlpatterns = [
	path('',HomePageView.as_view(),name='home'),
	path('index/',HomePageView.as_view(),name='index'),
	path('notes/',NotesPageView.as_view(),name='notes'),
	# path('dashboard/',DashboardPageView.as_view(),name='dashboard'),
	# path('login/',LoginPageView.as_view(),name='login'),
	# path('register/customer/',RegCustomerPageView.as_view(),name='regcustomer'),
	# path('register/product/',RegProductPageView.as_view(),name='regproduct'),
	# path('report/customer/',TableCustomerPageView.as_view(),name='tablecustomer'),
	# path('report/product/',TableProductPageView.as_view(),name='tableproduct'),
	# path('report/order/',TableOrderPageView.as_view(),name='tableorder'),
	# path('404/',ErrorPageView.as_view(),name='error'),
	path('main/',MainView.as_view(),name='main'),


]
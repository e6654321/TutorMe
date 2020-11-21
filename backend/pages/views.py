from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView

# Create your views here.

class HomePageView(TemplateView):
    template_name = 'index.html'

class MainView(TemplateView):
    template_name = 'main.html'

class NotesPageView(TemplateView):
    template_name='notes.html'
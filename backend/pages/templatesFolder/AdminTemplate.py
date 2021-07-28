from django.shortcuts import redirect
from .CommonUserTemplate import CommonUserTemplate


class AdminTemplate:
    def viewMentor(self):
        return redirect('pages:mentor')

    def viewMentee(self):
        return redirect('pages:mentee')

    def viewSchedule(self, request):
        return CommonUserTemplate.viewSchedule(self, request)


    def logout(self, request):
        return CommonUserTemplate.logout(self, request)

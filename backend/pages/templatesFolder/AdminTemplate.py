from django.shortcuts import redirect
from .CommonUserTemplate import CommonUserTemplate

class AdminTemplate:
<<<<<<< HEAD
  def viewMentor(self):
    return redirect('pages:mentor')
  
  def viewMentee(self):
    return redirect('pages:mentee')
  #viewSchedule
  def reqSchedule(self, request):
    return CommonUserTemplate.reqSchedule(self, request)
  
  def logout(self, request):
    return CommonUserTemplate.logout(self, request)
<<<<<<< HEAD
  
  
=======
=======
    def viewMentor(self):
        return redirect('pages:mentor')

    def viewMentee(self):
        return redirect('pages:mentee')

    def viewSchedule(self, request):
        return CommonUserTemplate.viewSchedule(self, request)

    def reqSchedule(self, request):
        return CommonUserTemplate.reqSchedule(self, request)

    def logout(self, request):
        return CommonUserTemplate.logout(self, request)
>>>>>>> parent of 4dc6284 (Fixed everything)
>>>>>>> 166e0146f03dd64d1451ae02639d72af374fe1a9

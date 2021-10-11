from datetime import date
from django.shortcuts import render, redirect
from django.contrib import messages
from ..templatesFolder.CommonUserTemplate import CommonUserTemplate

class ScheduleModel():
  subject = ""
  sched = date.today()
  rate = 0
  ulocation = [0,0]

  def getSubject(self):
    return self.subject

  def getTime(self):
    return self.sched

  def getRate(self):
    return self.rate
  
  def setSubject(self, subject):
    self.subject = subject

  def setTime(self, sched):
    self.sched = sched

  def setRate(self, rate):
    self.rate = rate
  #viewSchedule
  def schedViaGeo(self, ulocation):
    self.ulocation = ulocation
    return CommonUserTemplate.reqSchedule(self, ulocation)
  #viewSchedule
  def reqSched(self, request):
    return CommonUserTemplate.reqSchedule(self, request)
  
  def addSched(self, request):
    try:
      if (request.user.is_staff):
        return render(request, 'create-subject.html')
          
      messages.error(
        request, 'You are not a mentor. You will be redirected momentarily.')
      return render(request, 'create-subject.html')
    except:
      messages.error(
        request, 'You are not a mentor. You will be redirected momentarily.')
      return render(request, 'create-subject.html')
    
  def cancelSched(self):
    return self
  
  def pay(self):
    return self
  
  def addPNotes(self):
    return self
  
  def editPNotes(self):
    return self
  


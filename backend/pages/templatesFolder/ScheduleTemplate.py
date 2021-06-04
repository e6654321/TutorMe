from .CommonUserTemplate import CommonUserTemplate

class ScheduleTemplate:
  def viewGeolocation(self, request):
    return CommonUserTemplate.geolocation(self, request)
  
  def autoMatch(self):
    return self
    
  def viewPayment(self, request):
    return CommonUserTemplate.viewPayment(self, request)
    
  def viewPersonalNotes(self, request):
    return CommonUserTemplate.viewNotes(self, request)
  
  def logout(self, request):
    return CommonUserTemplate.logout(self, request)
from .CommonUserTemplate import CommonUserTemplate

class PaymentTemplate():
  def viewAmountDue(self):
    return self
  
  def viewSessionDetails(self):
    return self

  def logout(self, request):
    return CommonUserTemplate.logout(self, request)
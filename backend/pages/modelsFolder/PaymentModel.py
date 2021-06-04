
class PaymentModel():
  schedID = 0

  def pay(self):
    return self
  
  def getPayment(self, schedID):
    return schedID
  
  def setPaymentMethod(self, schedID):
    self.schedID = schedID
  
  def getPaymentMethod(self, schedID):
    return schedID
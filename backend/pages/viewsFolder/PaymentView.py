from ..templatesFolder.PaymentTemplate import PaymentTemplate
from ..modelsFolder.PaymentModel import PaymentModel

class PaymentView():
  paymentTemplate = PaymentTemplate
  paymentModel = PaymentModel

  def getPayment(self, schedID):
    self.paymentModel.getPayment(self, schedID)
    
  def pay(self, schedID):
    self.paymentModel.pay(self, schedID)
    
  def setPaymentMethod(self,):
    self.paymentModel.setPaymentMethod(self)
    
  def getPaymentMethod(self, schedID):
    self.paymentModel.getPaymentMethod(self, schedID)
    
  def updateTemplate(self):
    return self.paymentTemplate
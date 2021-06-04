from . import UserModel

class CommonUserModel(UserModel):
  cardOwnerName =  ""
  cardAccNumber = 0
  cardExpireMM = 0
  cardExpireYY = 0
  cardCVV = 0
  isAccountInfoChanged = False
  upcomingSchedules = False
  messages = []
  hasPushNotification = False
  hasEmailNotification = False

  def getCardOwnerName(self):
    return self.cardOwnerName

  def getCardAccNumber(self):
    return self.cardAccNumber

  def getCardExpireMM(self):
    return self.cardExpireMM
    
  def getCardExpireYY(self):
    return self.cardExpireYY

  def getCardCVV(self):
    return self.cardCVV
    
  def setCardOwnerName(self, cardOwnerName):
    self.cardOwnerName = cardOwnerName

  def setCardAccNumber(self, cardAccNumber):
    self.cardAccNumber = cardAccNumber

  def setCardExpireMM(self, cardAccNumber):
    self.cardAccNumber = cardAccNumber

  def setCardExpireYY(self, cardExpireYY):
    self.cardExpireYY = cardExpireYY
    
  def setCardCVV(self, cardCVV):
    self.cardCVV = cardCVV
  
  def setEmailNotifications(self, hasEmailNotification):
    self.hasEmailNotification = hasEmailNotification
    
  def setPushNotifications(self, hasPushNotification):
    self.hasPushNotification = hasPushNotification

  def sendMessage(self):
    return self.messages
  
  def recieveMessage(self, message):
    self.messages.push(message)
  
  def locate(self):
    return self
  
  def enterSearchString(self, searchString):
    return searchString
  
  def editNotes(self):
    return self

  def addNotes(self):
    return self
    
  def cancelSchedule(self):
    return self
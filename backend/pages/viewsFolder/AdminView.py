from ..templatesFolder.AdminTemplate import AdminTemplate
from ..modelsFolder.AdminModel import AdminModel

class AdminView:
  adminTemplate = AdminTemplate
  adminModel = AdminModel

  def addUser(self, user):
    return self.adminModel.addUser(self, user)
    
  def updateUser(self, user):
    return self.adminModel.updateUser(self, user)

  def removeUser(self, user):
    return self.adminModel.removeUser(self, user)
  
  def updateTemplate(self):
    return self.adminTemplate
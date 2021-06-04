from ..templatesFolder.CommonUserTemplate import CommonUserTemplate
from ..modelsFolder.CommonUserModel import CommonUserModel

class CommonUserView(CommonUserModel):
  userTemplate = CommonUserTemplate
  userModel = CommonUserModel

  def updateTemplate(self):
    return self.menteeTemplate
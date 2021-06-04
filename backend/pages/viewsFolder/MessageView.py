from ..templatesFolder.MessageTemplate import MessageTemplate
from ..modelsFolder.MessageModel import MessageModel

class MessageView():
  messageTemplate = MessageTemplate
  messageModel = MessageModel

  def deleteMessage(self):
    self.messageModel.deleteMessage(self)

  def deleteMessage(self, messages):
    self.messageModel.sendMessage(self, messages)

  def updateTemplate(self):
    return self.messageTemplate
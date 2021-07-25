from backend.pages.modelsFolder.MessageModel import MessageModel


class MessageTemplate():
  message = MessageModel
  
  def viewMessage(self):
    return self.message
class MessageModel():
  messages = []

  def deleteMessage(self):
    self.messages.pop()

  def sendMessage(self, messages):
    self.messages.append(messages)
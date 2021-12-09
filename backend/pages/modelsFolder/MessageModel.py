from django.db import models
from django.contrib.auth.models import User

class MessageModel(models.Model):
    messageID= models.AutoField(primary_key=True)
    dateSent = models.DateTimeField(auto_now_add=True, blank=True)
    senderId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='message_sender')
    recieverId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='message_reciever')

    message = models.TextField()
    readonly_fields = ('messageID', 'dateSent')

    class Meta:
        db_table = "Messages"
    
    def getMessage(self, mID):
        return self.objects.get(messageID=mID)
    
    def addMessage(self, senderId, recieverId, message):
        try:
            new_message= self()
            new_message.senderId=senderId
            new_message.recieverId=recieverId
            new_message.message=message
            new_message.save()
        except Exception as e:
            print(e)

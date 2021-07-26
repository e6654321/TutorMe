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
from pages.modelsFolder.MessageModel import MessageModel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from pages.models import Schedule
from django.shortcuts import render, redirect
from django.core import serializers
from pages.forms import MessageForm
from django.views.generic import TemplateView

class MessageView(TemplateView):
    def get(self, request):
        userId = request.user
        messageId = request.GET.get('id')

        if messageId:
            user = User.objects.get(id=messageId)
            sentMessages = MessageModel.objects.filter(senderId__id=userId.id, recieverId__id=messageId)
            recievedMessages = MessageModel.objects.filter(recieverId__id=userId.id, senderId__id=messageId)
            messages = sentMessages | recievedMessages
            print(messages.order_by('dateSent'))
            data = {
                "user": user,
                "messages": messages.order_by('dateSent'),
            }
            return render(request, 'messaging.html', data)
        else:
            if userId.is_staff:
                userIds = Schedule.objects.filter(subject__mentorID_id=userId).order_by('id').values('userID_id')
            else:
                userIds = Schedule.objects.filter(userID_id=userId).order_by('id').values('subject__mentorID_id')
            users = User.objects.filter(id__in=userIds)
            data = {
                "users": users,
            }
            
            return render(request, 'messages.html', data)

    def post(self, request):
        recieverId = request.POST.get("userId")
        message = request.POST.get("message")
        reciever = User.objects.get(id=recieverId)
        MessageModel.objects.create(message=message, senderId=request.user, recieverId=reciever)
        
        return HttpResponseRedirect('/messaging/?id='+recieverId)
        
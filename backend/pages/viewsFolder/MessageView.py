from pages.modelsFolder.MessageModel import MessageModel
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from pages.models import Schedule
from django.shortcuts import render, redirect
from django.core import serializers
from pages.forms import MessageForm
from django.views.generic import TemplateView
from pages.models import Mentor
from pages.models import Mentee
from pages.models import Subject

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
        mentorID = Mentor.objects.get(user_identification_id=userId)
        menteeIds = Schedule.objects.filter(subject__mentorID_id=mentorID).order_by('id').values('menteeID')
        userIds= Mentee.objects.filter(menteeID__in=menteeIds).order_by('menteeID').values('user_identification_id')
        
      else:
        mentee_ID = Mentee.objects.get(user_identification_id=userId)
        subjectIds = Schedule.objects.filter(menteeID=mentee_ID).order_by('id').values('subject_id')
        mentorIds = Subject.objects.filter(id__in=subjectIds).order_by('mentorID_id').values('mentorID_id')
        userIds = Mentor.objects.filter(mentorID__in=mentorIds).order_by('mentorID').values('user_identification_id')
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
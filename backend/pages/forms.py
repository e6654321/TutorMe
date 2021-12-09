from django.db.models import fields
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Details, Account, Notes, Subject, Receipt, Schedule, Mentee, Mentor, Profile
from django import forms
from pages.modelsFolder.MessageModel import MessageModel


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2','is_staff']


class CreateMenteeForm(ModelForm):
    class Meta:
        model = Mentee
        fields = '__all__'



class CreateMentorForm(ModelForm):
    class Meta:
        model = Mentor
        fields = '__all__'

class CreateProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'



class CardDetailsForm(ModelForm):
    class Meta:
        model = Details
        fields = '__all__'


class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = '__all__'


class CreateSubjectForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ['mentorID']
        fields = '__all__'


class RequestSchedForm(ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

class ReceiptForm(ModelForm):
    class Meta:
        model= Receipt
        fields = '__all__'

class NotesForm(ModelForm):
    class Meta:
        model = Notes
        fields= ['notesTitle', 'menteeID', 'subjectID', 'notes']
    
    def getNotesID(self):
        return self.data['notesID']

    def getNotesTitle(self):
        return self.data['notesTitle']

    def getMenteeID(self):
        return self.data['menteeID']

    def getSubjectID(self):
        return self.data['subjectID']

class MessageForm(ModelForm):
    class Meta:
        model = MessageModel
        fields = '__all__'

    def getSenderID(self):
        return self.data['senderId']

    def getRecieverID(self):
        return self.data['recieverId']

    def getMessage(self):
        return self.data['message']

    def getDateSent(self):
        return self.data['dateSent']

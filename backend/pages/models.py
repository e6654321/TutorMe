from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
# Create your models here.

class Profile(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contactNo = models.IntegerField(blank=True, null=True)
    #userID = models.AutoField(primary_key=True, default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Profile"


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.create(user=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()


class Admin(Profile):
    #adminID = models.AutoField(primary_key=True, default=None)
    position = models.CharField(
        max_length=50, blank=False, null=False, default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Admin"


class Mentee(models.Model):
    menteeID = models.AutoField(primary_key=True)
    user_identification = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    bio = models.CharField(max_length=100, blank=False,
                           null=False, default=None)
    def addMentee(bio, userID):
        try:
            newMentee = Mentee()
            newMentee.bio = bio
            newMentee.user_identification=userID
            newMentee.save()
            print('saved')
        except Exception as e:
            print(e)
    
    class Meta:
        db_table = "Mentee"


class Mentor(models.Model):
    mentorID = models.AutoField(primary_key=True)
    user_identification = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    achvemnts = models.BooleanField()
    proofs = models.BooleanField()

    def addMentor(achvements, proofs, userID):
        try:
            newMentor = Mentor()
            newMentor.achvemnts=achvements
            newMentor.proofs=proofs
            newMentor.user_identification=userID
            newMentor.save()
            print('saved')
        except Exception as e:
            print(e)
    
    class Meta:
        db_table = "Mentor"

class Subject(models.Model):
    #subjectID = models.AutoField(primary_key=True, default=None)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
    subjectName = models.CharField(max_length=100, default='')
    ratePerHour = models.DecimalField(
        max_digits=5, decimal_places=2, default='0')
    session_date = models.DateField(blank=True, null=True)
    session_time_end = models.CharField(max_length=10,  default='00:00')
    session_time_start = models.CharField(max_length=10, default='00:00')
    category = models.CharField(max_length=30, default='')
    readonly_fields = ('id',)
    latitude = models.FloatField(default=10.3344277)
    longitude = models.FloatField(default=123.8791918)

    class Meta:
        db_table = "Subject"


class Schedule(models.Model):
    #scheduleId = models.AutoField(primary_key=True, default=None)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True, null=True)
    time = models.CharField(max_length=10,  default='00:00-00:00', null=True)
    custom_time_start = models.CharField(
        max_length=10,  default='00:00', null=True)
    custom_time_end = models.CharField(
        max_length=10,  default='00:00', null=True)
    ratePrHour = models.DecimalField(
        max_digits=5, decimal_places=2, default='0', null=True)
    payment_method = models.CharField(max_length=10,  default='', null=True)
    status = models.BooleanField(default=False)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Schedule"


class TutorialPayment(models.Model):
    #TPaymentID = models.AutoField(primary_key=True, default=None)
    id = models.AutoField(primary_key=True, default=None)
    scheduleID = models.ForeignKey(
        Schedule, null=True, on_delete=models.SET_NULL)
    total = models.FloatField()
    readonly_fields = ('id',)

    class Meta:
        db_table = "TutorialPayment"


class Details(models.Model):
    #detailID = models.AutoField(primary_key=True, default=None)
    cardOwnerName = models.TextField(max_length=100, default=None)
    cardNumber = models.IntegerField(default=None, blank=True, null=True)
    expire_month = models.IntegerField(default=None, blank=True, null=True)
    expire_year = models.IntegerField(default=None, blank=True, null=True)
    cvc = models.IntegerField(default=None, blank=True, null=True)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Details"


class Receipt(models.Model):
    #receiptID = models.AutoField(primary_key=True, default=None)
    receipt = models.CharField(max_length=100, default='')
    readonly_fields = ('id',)

    class Meta:
        db_table = "Receipt"


class Account(models.Model):
    #accountID = models.AutoField(primary_key=True, default=None)
    userID = models.ForeignKey(User, null=True, blank=False, on_delete=models.SET_NULL)
    detailID = models.ForeignKey(Details, null=True, blank=False, on_delete=models.SET_NULL)
    receiptID = models.ForeignKey(Receipt, null=True, blank=False, on_delete=models.SET_NULL)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Account"


class Messages(models.Model):
    #messageID = models.AutoField(primary_key=True, default=None)
    messageID = models.AutoField(primary_key=True, default=0)
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    
    message = models.TextField()
    readonly_fields = ('id',)

    class Meta:
        db_table = "Messages"


class Ratings(models.Model):
    #ratingID = models.AutoField(primary_key=True, default=None)
    rate = models.IntegerField()
    readonly_fields = ('id',)

    class Meta:
        db_table = "Ratings"


class Comments(models.Model):
    #commentID = models.AutoField(primary_key=True, default=None)
    comment = models.TextField()
    readonly_fields = ('id',)

    class Meta:
        db_table = "Comments"


class Review(models.Model):
    #reviewID = models.AutoField(primary_key=True, default=None)
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
    ratings = models.ForeignKey(Ratings, null=True, on_delete=models.SET_NULL)
    comments = models.ForeignKey(
        Comments, null=True, on_delete=models.SET_NULL)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Review"


class Notes(models.Model):

    notesID= models.AutoField(primary_key=True, default=0)
    notesTitle = models.CharField(max_length=500, default='Title' )
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
    subjectID = models.ForeignKey(
        Subject, null=True, on_delete=models.SET_NULL)
    notes = models.FileField(validators=[FileExtensionValidator(allowed_extensions=['pdf', 'docx', 'txt'])],null=True, blank=True)
    

    class Meta:
        db_table = "Notes"

from django.db import models
from django.utils import timezone
from datetime import datetime

# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=100, blank=False, null=False, unique=True)
    password = models.CharField(max_length=50, blank=False, null=False, default=None)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contactNo = models.IntegerField(blank=True, null=True)
    #userID = models.AutoField(primary_key=True, default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "User"


class Admin(User):
    #adminID = models.AutoField(primary_key=True, default=None)
    position = models.CharField(max_length=50, blank=False, null=False, default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Admin"


class Mentee(User):
    #menteeID = models.AutoField(primary_key=True, default=None)
    bio = models.CharField(max_length=100, blank=False, null=False, default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Mentee"


class Mentor(User):
    #mentorID = models.AutoField(primary_key=True, default=None)
    achvemnts = models.BooleanField()
    proofs = models.BooleanField()
    readonly_fields = ('id',)

    class Meta:
        db_table = "Mentor"


class Subject(models.Model):
    #subjectID = models.AutoField(primary_key=True, default=None)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
    subjectName = models.CharField(max_length=100)
    ratePerHour = models.DecimalField(max_digits=5, decimal_places=2, default='0')
    session_date = models.DateField(default=None)
    session_time = models.TimeField(default=None)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Subject"


class Schedule(models.Model):
    #scheduleId = models.AutoField(primary_key=True, default=None)
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    curr_date = models.DateTimeField(default=datetime.now, blank=True)
    curr_time = models.DateTimeField(default=datetime.now, blank=True)
    status = models.BooleanField(default=False)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Schedule"


class TutorialPayment(models.Model):
    #TPaymentID = models.AutoField(primary_key=True, default=None)
    id = models.AutoField(primary_key=True, default=None)
    scheduleID = models.ForeignKey(Schedule, null=True, on_delete=models.SET_NULL)
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
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    detailID = models.ForeignKey(Details, null=True, on_delete=models.SET_NULL)
    receiptID = models.ForeignKey(Receipt, null=True, on_delete=models.SET_NULL)
    readonly_fields = ('id',)

    class Meta:
        db_table = "Account"


class Messages(models.Model):
    #messageID = models.AutoField(primary_key=True, default=None)
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

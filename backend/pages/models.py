from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    userName = models.CharField(max_length=100, blank=False, null=False)
    firstName = models.CharField(max_length=100, blank=True, null=True)
    middleName = models.CharField(max_length=100, blank=True, null=True)
    lastName = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contactNo = models.IntegerField(null=True)
    userID = models.IntegerField(null=True)

    class Meta:
        db_table = "User"


class Admin(User):
    adminID = models.IntegerField(null=True)

    class Meta:
        db_table = "Admin"


class Mentee(User):
    menteeID = models.IntegerField(null=True)

    class Meta:
        db_table = "Mentee"


class Mentor(User):
    mentorID = models.IntegerField(null=True)
    achvemnts = models.BooleanField()
    proofs = models.BooleanField()

    class Meta:
        db_table = "Mentor"


class Subject(models.Model):
    subjectID = models.IntegerField(null=True)
    subjectName = models.CharField(max_length=100)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "Subject"


class Schedule(models.Model):
    scheduleId = models.IntegerField()
    subject = models.ForeignKey(Subject, null=True, on_delete=models.SET_NULL)
    session_date = models.DateField()
    session_time = models.TimeField()
    curr_date = models.DateField(default=timezone.localdate)
    curr_time = models.DateField(default=timezone.localtime)
    status = models.BooleanField(default=False)
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "Schedule"


class TutorialPayment(models.Model):
    TPaymentID = models.IntegerField(primary_key=True)
    scheduleID = models.ForeignKey(
        Schedule, null=True, on_delete=models.SET_NULL)
    total = models.FloatField()

    class Meta:
        db_table = "TutorialPayment"


class Details(models.Model):
    detailID = models.IntegerField()
    mode = models.CharField(max_length=100)

    class Meta:
        db_table = "Details"


class Receipt(models.Model):
    receiptID = models.IntegerField()
    userID = models.IntegerField()

    class Meta:
        db_table = "Receipt"


class Account(models.Model):
    accountID = models.IntegerField()
    userID = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    detailID = models.ForeignKey(Details, null=True, on_delete=models.SET_NULL)
    receiptID = models.ForeignKey(
        Receipt, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "Account"


class Messages(models.Model):
    messageID = models.IntegerField()
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    message = models.TextField()

    class Meta:
        db_table = "Messages"


class Ratings(models.Model):
    ratingID = models.IntegerField()
    rate = models.IntegerField()

    class Meta:
        db_table = "Ratings"


class Comments(models.Model):
    commentID = models.IntegerField()
    comment = models.TextField()

    class Meta:
        db_table = "Comments"


class Review(models.Model):
    reviewID = models.IntegerField()
    menteeID = models.ForeignKey(Mentee, null=True, on_delete=models.SET_NULL)
    mentorID = models.ForeignKey(Mentor, null=True, on_delete=models.SET_NULL)
    ratings = models.ForeignKey(Ratings, null=True, on_delete=models.SET_NULL)
    comments = models.ForeignKey(
        Comments, null=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "Review"

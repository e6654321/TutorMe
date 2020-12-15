from django.contrib import admin
from . import models
from django.contrib.auth.models import User

# Register your models here.
admin.site.unregister(User)
admin.site.register(models.Profile)
admin.site.register(models.Admin)
admin.site.register(models.Mentee)
admin.site.register(models.Mentor)
admin.site.register(models.Subject)
admin.site.register(models.Schedule)
admin.site.register(models.TutorialPayment)
admin.site.register(models.Details)
admin.site.register(models.Receipt)
admin.site.register(models.Account)
admin.site.register(models.Messages)
admin.site.register(models.Ratings)
admin.site.register(models.Comments)
admin.site.register(models.Review)
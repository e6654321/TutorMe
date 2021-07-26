from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.core import serializers
from ..models import Details, Notes, Profile, Subject, Schedule, Account, Mentee
from itertools import chain


class CommonUserTemplate:
    def viewProfile(self, request):
        current_user = request.user
        user = User.objects.filter(id=current_user.id)
        profile = Profile.objects.filter(user=current_user)
        user[0].refresh_from_db()
        if(profile):
            return render(request, 'profile.html', {
                "user": user[0],
                "profile": profile[0],
            })
        else:
            profile = {}
            print("blank profile")
            print(profile)

            return render(request, 'profile.html', {
                "user": user[0],
                "profile": profile,
            })

    def viewPayment(self, request):
        current_user = request.user
        print("user")
        acc = Account.objects.filter(userID=current_user)
        print(acc)
        if acc.exists():
            s1 = Account.objects.filter(userID=current_user)
            hasValue = bool(s1.values()[0].get('detailID_id'))

            if(hasValue):
                details = s1.values('detailID__id', 'detailID__cardOwnerName', 'detailID__cardNumber',
                                    'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
            else:
                details = [Details()]
            data = {
                "details": details
            }
            print('get')
            print([details])
            return render(request, 'payment.html', data)
        else:
            return redirect('pages:addpayment')

    def viewSettings(self):
        return 'settings.html'

    def logout(self, request):
        logout(request)
        return redirect('pages:login')

    def viewMessages(self):
        return redirect('pages:messages')

    def geolocation(self, request):
        json_serializer = serializers.get_serializer("json")()
        scheds = json_serializer.serialize(
            Schedule.objects.all().order_by('id'))
        mentor = json_serializer.serialize(
            User.objects.all().order_by('id'))
        subjects = json_serializer.serialize(
            Subject.objects.all().order_by('id'))
        data = {
            "scheds": scheds,
            "mentor": mentor,
            "subjects": subjects,
        }
        return render(request, 'geolocation.html', data)

    def search(self, request):
        userId = request.user
        queries = [((Q(id=sched.subject.id)) if userId.id== sched.menteeID_id else (Q(id=0))) for sched in Schedule.objects.all()]
        try:
          query = queries.pop()
          for item in queries:
              query |= item
          s1 = Subject.objects.exclude(query).values('id','subjectName', 'ratePerHour',
            'session_date', 'session_time_start', 'session_time_end',
            'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')
        except IndexError as e:
            s1 = Subject.objects.all().values('id','subjectName', 'ratePerHour',
              'session_date', 'session_time_start', 'session_time_end',
              'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')
        data = {
          "subject": s1.exclude(mentorID__user_identification_id=userId.id)
        }
        return render(request, 'search.html', data)

    def viewNotes(self, request):
        user = request.user.id
        try:
          menteeID = Mentee.objects.get(user_identification_id=user)
          sched = Schedule.objects.filter(menteeID_id=menteeID)
          subjectList= []
          for p in sched:
            subjectList.append(Subject.objects.get(pk=p.subject_id))
            print(subjectList)
          n = Notes.objects.filter(menteeID_id=menteeID)
          data = {
            "notes": n,
            "subject": subjectList
          }
        except Exception as e:
          data={}
        return render(request, 'notes.html', data)
    

    def reqSchedule(self, request):
        schedId = request.GET.get('id')
        print("Sched Id: " + str(schedId))
        sub = Subject.objects.filter(id=schedId).values('id','mentorID', 'subjectName', 'ratePerHour',
                                                        'session_date', 'session_time_end', 'session_time_start', 'category', 'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')

        profile = Profile.objects.filter(user_id=request.user.id)
        account = Account.objects.filter(userID_id=request.user.id)
        cardId = account.values('detailID_id')
        card = Details.objects.filter(id=cardId)
        subject = {
            'subject': sub,
            'profile': profile,
            'card': card
        }
        return render(request, 'RequestSched.html', subject)

    def viewNotifications(self):
        return redirect('pages:notifications')

    def chatbot(self):
        return redirect('pages:chatbot')

    def becomeMentor(self):
        return redirect('pages:become-mentor')

    def history(self, request):
        userId = request.user
        queries = [((Q(id=sched.subject.id)) if userId.id == sched.menteeID_id else (
            Q(id=0))) for sched in Schedule.objects.all()]
        try:
            query = queries.pop()
            for item in queries:
                query |= item
            s1 = Subject.objects.exclude(query).values('id', 'subjectName', 'ratePerHour',
                                                       'session_date', 'session_time_start', 'session_time_end',
                                                       'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')
        except IndexError as e:
            s1 = Subject.objects.all().values('id', 'subjectName', 'ratePerHour',
                                              'session_date', 'session_time_start', 'session_time_end',
                                              'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')
        data = {
            "subject": s1
        }
        return render(request, 'history.html', data)

    def viewSchedule(self, request):
        schedId = request.GET.get('id')
        print("Sched Id: " + str(schedId))
        sub = Subject.objects.filter(id=schedId).values('id', 'mentorID', 'subjectName', 'ratePerHour',
                                                        'session_date', 'session_time_end', 'session_time_start', 'category', 'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name')

        sched = Schedule.objects.filter(id=schedId).values('menteeID_id', 'ratePrHour', 'time', 'ratePrHour',
                                                           'custom_time_start', 'custom_time_end', 'payment_method', 'status', 'menteeID__user_identification__first_name', 'menteeID__user_identification__last_name')

        print(sched)
        profile = Profile.objects.filter(user_id=request.user.id)
        account = Account.objects.filter(userID_id=request.user.id)
        cardId = account.values('detailID_id')
        card = Details.objects.filter(id=cardId)
        subject = {
            'subject': sub,
            'profile': profile,
            'card': card,
            'sched': sched
        }
        return render(request, 'ViewSched.html', subject)

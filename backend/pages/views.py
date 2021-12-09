from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile, Schedule, Subject, Mentor, Mentee, Details, Account, Notes, Receipt, Review, Ratings, Comments
from .forms import CreateUserForm, CreateProfileForm, CardDetailsForm, AccountForm, CreateSubjectForm, NotesForm, ReceiptForm, CreateMenteeForm, CreateMentorForm
from django.db.models import Q
from django.core import serializers
import json
from django.core.serializers.json import DjangoJSONEncoder

from .modelsFolder.AdminModel import AdminModel
from .modelsFolder.ScheduleModel import ScheduleModel
from .templatesFolder.AdminTemplate import AdminTemplate
from .templatesFolder.CommonUserTemplate import CommonUserTemplate
from.templatesFolder.RatingFeedbackTemplate import RatingFeedbackTemplate
from .modelsFolder.NotesModel import NotesModel
from .modelsFolder.MenteeModel import MenteeModel
from .modelsFolder.MentorModel import MentorModel
from .templatesFolder.RatingFeedbackTemplate import RatingFeedbackTemplate
from .modelsFolder.RatingFeedbackModel import RatingFeedbackModel

from django.http import JsonResponse
import json

import stripe
stripe.api_key = "sk_test_51J9TM9L6zwlGFb0jpsul8bsQLGExhhTrPXyymygvzUREf3GO2Bc1W6Pu2vl68IMAq9dNzv786KoRyyrnRn3hbZ0I00Oz1NePik"
class HomePageView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'search.html')
        return render(request, 'index.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('pages:search')
        else:
            messages.info(request, "Username or password incorrect")
            return render(request, 'index.html')


class RegisterView(TemplateView):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'search.html')
        form = CreateUserForm()
        context = {'form': form}
        return render(request, 'register.html', context)

    def post(self, request):
        form = request.POST.copy()
        form = AdminModel.addUser(self, form)
        try:
            usn = form.cleaned_data.get('username')
            id= User.objects.get(username=usn)
            usn = form.cleaned_data.get('username')
            id= User.objects.get(username=usn)
            mentor = form.cleaned_data.get('is_staff')
            if mentor==True:
                Mentor.addMentor(achvements=True, proofs=True, userID = id)
            else:
                Mentee.addMentee(bio="hello", userID= id)
        except Exception as e:
            print(e)
        if form:
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account created ' + username)
            return redirect('pages:login')
        else:
            form = CreateUserForm()
            messages.error(request, 'Check inputs and try again')

        context={'form': form}
        return render(request, 'register.html', context)


class logoutUser(TemplateView):
    def get(self, request):
        return AdminTemplate.logout(self, request)

class MainView(TemplateView):
    template_name = 'main.html'

def paymentComplete(request):
    body = json.loads(request.body)
    print('BODY:', body)

    return JsonResponse('Payment completed!', safe=False)
#viewSchedule
class RequestSchedView(TemplateView):
    def get(self, request):
        return AdminTemplate.reqSchedule(self, request)

    def post(self, request):
        if request.method == 'POST':
            mode =  request.POST.get('cardMode')
            subjectID = request.POST.get("subjectID")
            # print(subjectID)

            subject = Subject.objects.filter(id=subjectID)
            ratePrHour = subject.values('ratePerHour')[0].get('ratePerHour')
            cardOwnerName = request.POST.get('cardOwnerName')
            cardEmail = request.POST.get('cardEmail')
            # print(ratePrHour)

            if 'com' in request.POST:
                mode = 'Cash on Delivery'
            elif mode == 'card':
                mode = 'Credit Card'
                if Details.objects.filter(cardOwnerName=cardOwnerName).exists():

                    
                    data = Details.objects.filter(cardOwnerName=cardOwnerName)
                    stripeCustomerID = data.values('stripeCustomerID')[0].get('stripeCustomerID')


                    charge = stripe.Charge.create(
                        customer=stripeCustomerID,
                        amount=int(ratePrHour)*100,
                        currency='usd',
                        description="Tutorial Session"
                        )
                else:
                    cname = request.POST['cardOwnerName']
                    customer = stripe.Customer.create(
                        name=cname,
                        email=request.POST['cardEmail'],
                        source=request.POST['stripeToken'] 
                        )

                    charge = stripe.Charge.create(
                        customer=customer,
                        amount=int(ratePrHour)*100,
                        currency='usd',
                        description="Tutorial Session"
                        )

                    Details.addDetails(cardOwnerName=cname, stripeCustomerID=customer.id)

        # if request.method == 'POST':
        #     subjectID = request.POST.get("subjectID")
        #     print(subjectID)
        #     mode = 'E-Wallet'

        #     if 'com' in request.POST:
        #         mode = 'Cash on Delivery'
        #     elif 'card-btn' in request.POST:
        #         mode = 'Credit Card'
        #     subject = Subject.objects.filter(id=subjectID)
        #     date = subject.values('session_date')[0].get('session_date')
        #     ratePrHour = subject.values('ratePerHour')[0].get('ratePerHour')
        #     time = (subject.values('session_time_start')[0].get('session_time_start'))+ " - " +(subject.values('session_time_end')[0].get('session_time_end'))
        #     print(time)
        #     custom_time_start = request.POST.get("timepicker")
        #     custom_time_end = request.POST.get("timepicker1")

        #     current_user = request.user
        #     menteeID = User.objects.get(username=current_user)
        #     menteeID = Mentee.objects.get(user_identification_id=menteeID)

        #     form = Schedule(subject=subject[0],menteeID=menteeID,date=date,ratePrHour=ratePrHour, time=time, custom_time_start=custom_time_start,
        #                     custom_time_end=custom_time_end, payment_method=mode)
        #     form.save()

            return redirect('pages:search')
        else:
            return HttpResponse('failed')

class NotesPageView(View):
    def createNotes(request):
        if request.method == 'POST':
            print(request.POST)
            if 'addNotes' in request.POST:
                print("add")
                form= NotesForm(request.POST, request.FILES)
                if form.is_valid():
                    notes_title= form.getNotesTitle()
                    userID = form.getMenteeID()
                    subjectID= form.getSubjectID()                  
                    notes_menteeID= Mentee.objects.get(user_identification_id=userID)
                    notes_subjectID= Subject.objects.get(id=subjectID)
                    notes_mentorID = Mentor.objects.get(mentorID=notes_subjectID.mentorID_id)
                    notes_note= request.FILES['notes']
                    NotesModel.addNotes(notes_menteeID, notes_mentorID, notes_subjectID, notes_title, notes_note)
                    messages.success(request, ("Notes added"))
                else:
                    messages.error(request, form.errors)
                    print(form.errors)
        return redirect('pages:notes')

    def removeNote(request):
        if request.method=='POST':
            print(request.POST)
            if 'deleteNote' in request.POST:
                form= NotesForm(request.POST or None)
                notesID= form.getNotesID()
                print(notesID)
                NotesModel.removeNotes(notesID)
                messages.success(request, ("Notes removed"))
        return redirect("pages:notes")

    @classmethod
    def viewNotes(self, request):
        return CommonUserTemplate.viewNotes(self, request)

    # def updateTemplate(self, request):
    #     if 'btnSort' in request.POST:
    #         item = request.POST.get("search")
    #         sort = request.POST.get("sort")
    #         print(sort)
    #         if sort == 'subjectName':
    #             sort = 'subjectID_id__subjectName'
    #         if sort == 'ratePerHour':
    #             sort = 'subjectID_id__ratePerHour'
    #         if sort == '-subjectName':
    #             sort = '-subjectID_id__subjectName'
    #         if sort == '-ratePerHour':
    #             sort = '-subjectID_id__ratePerHour'
    #         n = Notes.objects.all()
    #         n = n.filter(Q(subjectID_id__subjectName__icontains=item) | Q(mentorID_id__user_identification__first_name__icontains=item)
    #                     | Q(mentorID_id__user_identification__last_name__icontains=item)).values('subjectID_id__subjectName',
    #                                                                     'mentorID_id__user_identification__first_name', 'mentorID_id__user_identification__last_name', 'subjectID_id__ratePerHour', 'notes', 'notesTitle').order_by(sort)
    #         data = {
    #             "notes": n
    #         }
    #         return render(request, 'notes.html', data)


class SearchView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.search(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
                print(sort)
                userId = request.user.id
                queries = [((Q(id=sched.subject.id)) if userId == sched.menteeID_id else (Q(id=0))) for sched in Schedule.objects.all()]
                s1 = Subject.objects.filter(Q(subjectName__icontains=item) | Q(mentorID_id__user_identification_id__first_name__icontains=item)
                                        | Q(mentorID_id__user_identification_id__last_name__icontains=item))
                print(s1)
                try:
                    query = queries.pop()
                    for item in queries:
                        query |= item
                    print(query)
                    s2 =s1.filter(~query).distinct()
                except IndexError as e:
                    s2 = s1.filter()
                print(s2)
                data = {
                    "subject": s2.values('id','subjectName', 'ratePerHour',
                                            'session_date', 'session_time_start', 'session_time_end',
                                            'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name').order_by(sort)
                }
                return render(request, 'search.html', data)


class GeolocationView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.geolocation(self, request)


class ProfileView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.viewProfile(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnUpdate' in request.POST:
                res = AdminModel.updateUser(self, request)
                return render(request, 'profile.html', {
                    "user": res[0],
                    "profile": res[1],
                })
            elif 'cancelUpdate' in request.POST:
                return redirect('pages:profile')


class PaymentView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.viewPayment(self, request)

    def post(self, request):
        if request.method == 'POST':
            print(request.POST)
            if 'btnUpdateCard' in request.POST:
                print("Update detail button clicked!")
                did = request.POST.get('did')
                print(did)
                cardOwnerName = request.POST.get('cardOwnerName')
                cardNum = request.POST.get('cardNum')
                month = request.POST.get('month')
                year = request.POST.get('year')
                cvc = request.POST.get('cvc')
                if (did):
                    Details.objects.filter(id=did).update(cardOwnerName=cardOwnerName,cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                    
                    s1 = Account.objects.filter(userID=request.user)
                    details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                        'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                    print(details)
                    data = {
                        "details": details
                    }
                    return render(request, 'payment.html', data)
                else:
                    details = Details(cardOwnerName=cardOwnerName,cardNumber=cardNum, expire_month=month, expire_year=year, cvc=cvc)
                    details.save()
                    print(details.id)

                    Account.objects.filter(userID=request.user).update(detailID=details)
                    s1 = Account.objects.filter(userID=request.user)
                    details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                        'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
                    print(details)
                    data = {
                        "details": [details]
                    }
                    return render(request, 'payment.html', data)
            elif 'btnDeleteCard' in request.POST:
                print("Delete product button clicked!")
                did = request.POST.get('did')
                rid = request.POST.get('rid')
                aid = request.POST.get('aid')
                if (did):
                    details = Details.objects.filter(pk = did).delete()
                    print(details)
                if (rid):
                    receipt = Receipt.objects.filter(pk = rid).delete()
                    print(receipt)
                if (aid):
                    acc = Account.objects.filter(pk = aid).delete()
                    print(acc)
                print("Record deleted!")
                return redirect('pages:addpayment')


class AddPaymentView(TemplateView):
    def get(self, request):
        return render(request, 'addpayment.html')

    def post(self, request):
        current_user = request.user
        cardOwnerName = request.POST.get('cardOwnerName')
        cardNum = request.POST.get('cardNumber')
        month = request.POST.get('expire_month')
        year = request.POST.get('expire_year')
        cvc= request.POST.get('cvc')
        # form = Details(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
        #                 expire_month=month, expire_year=year, cvc=cvc)
        accForm = Account(userID=current_user)
        print(cvc)
        form = CardDetailsForm(request.POST)
        if form.is_valid():
            form.save()
            accForm.save()

            saved_details = Details.objects.filter(cardOwnerName=cardOwnerName, cardNumber=cardNum, 
                        expire_month=month, expire_year=year, cvc=cvc)
            print(saved_details)
            Account.objects.filter(userID=current_user).update(detailID=saved_details[0])
            s1 = Account.objects.filter(userID=current_user)
            details = s1.values('detailID__id','detailID__cardOwnerName', 'detailID__cardNumber', 
                'detailID__expire_month', 'detailID__expire_year', 'detailID__cvc')
            print(details)
            data = {
                "details": [details]
            }
            return render(request, 'payment.html', data)
        else:
            messages.error(request, 'Check inputs and try again')
            return render(request, 'addpayment.html')


class SettingsView(TemplateView):
    template_name = CommonUserTemplate.viewSettings('')


class MessagingView(TemplateView):
    template_name = 'messaging.html'


class CreateSubjectView(TemplateView):
    # template_name= 'create-subject.html'
    def get(self, request):
        return ScheduleModel.addSched(self, request)

    def post(self, request):
        form = CreateSubjectForm(request.POST)
        print(form.errors)
        mentors = ''
        if request.user.is_authenticated:
            current_user = request.user
            mentorID = User.objects.get(username=current_user)
            print(mentorID.id)
            mentorID = Mentor.objects.get(user_identification=mentorID)

        if form.is_valid:
            subName = request.POST.get('subjectName')
            subDate = request.POST.get('session_date')
            timeStart = request.POST.get('session_time_start')
            timeEnd = request.POST.get('session_time_end')
            rate = request.POST.get('ratePerHour')
            category = request.POST.get('category')
            latitude = request.POST.get('latitude')
            longitude = request.POST.get('longitude')
            print(latitude,longitude)
            form = Subject(subjectName=subName,  session_date=subDate,
                           session_time_start=timeStart, session_time_end=timeEnd,
                           ratePerHour=rate, category=category, mentorID=mentorID,
                           latitude=latitude, longitude=longitude
                           )
            print(form.mentorID)
            form.save()
            return redirect('pages:search')
        else:
            messages.error(request, 'Check inputs and try again')
            print(form.errors)
            return render(request, 'create-subject.html')


class ScheduleSubjectView(TemplateView):
    template_name = 'schedule-page.html'


class MentorProfileView(TemplateView):
    template_name = 'mentor-profile.html'


class ChatBotView(TemplateView):
    template_name = 'Chatbot.html'

class RatingFeedback(TemplateView):
    def get(self, request):
        return RatingFeedbackTemplate.viewReview(self, request)

    def post(self, request):
        if request.method == 'POST':
            rating = request.POST.get("rate")
            comments = request.POST.get("message")

            rate = RatingFeedbackModel.setRating(rating)
            comment = RatingFeedbackModel.setFeedback(comments)
            form = Review(ratings=rate, comments=comment)
            form.save()
            print(form)
            return redirect('pages:RatingFeedback')
        else:
            return HttpResponse('failed')
class HistoryView(TemplateView):
    def get(self, request):
        return CommonUserTemplate.history(self, request)

    def post(self, request):
        if request.method == 'POST':
            if 'btnSort' in request.POST:
                item = request.POST.get("search")
                sort = request.POST.get("sort")
                print(sort)
                userId = request.user.id
                queries = [((Q(id=sched.subject.id)) if userId == sched.menteeID_id else (
                    Q(id=0))) for sched in Schedule.objects.all()]
                s1 = Subject.objects.filter(Q(subjectName__icontains=item) | Q(mentorID_id__user_identification_id__first_name__icontains=item)
                                            | Q(mentorID_id__user_identification_id__last_name__icontains=item))
                print(s1)
                try:
                    query = queries.pop()
                    for item in queries:
                        query |= item
                    print(query)
                    s2 = s1.filter(~query).distinct()
                except IndexError as e:
                    s2 = s1.filter()
                print(s2)
                data = {
                    "subject": s2.values('id', 'subjectName', 'ratePerHour',
                                         'session_date', 'session_time_start', 'session_time_end',
                                         'mentorID__user_identification__first_name', 'mentorID__user_identification__last_name').order_by(sort)
                }
                return render(request, 'history.html', data)


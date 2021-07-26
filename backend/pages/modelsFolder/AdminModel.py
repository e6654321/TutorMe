from ..models import Profile
from django.contrib.auth.models import User
from ..forms import CreateUserForm

class AdminModel():
  user = User

  def addUser(self, user):
    form = CreateUserForm(user)
    if form.is_valid():
      newUser = form.save()
      newUser.refresh_from_db()
      if (form.cleaned_data['is_staff']):
          newUser.first_name = 'Mentor'
          newUser.last_name = 'Mentor'
      else:
          newUser.first_name = 'Mentee'
          newUser.last_name = 'Mentee'
      newUser.save()
      print(newUser)
      return form
    else:
      print(form.errors)
      return False
    
  def updateUser(self, request):
    fname = request.POST.get('fname')
    mname = request.POST.get('mname')
    lname = request.POST.get('lname')
    email = request.POST.get('email')
    number = request.POST.get('number')
    username = request.POST.get('username')
    User.objects.filter(
            id=request.user.id
        ).update(first_name=fname,last_name=lname, email=email, username=username)
    
    
    profile = Profile.objects.filter(user=request.user)

    if profile.exists():
        profile.update(middleName=mname,contactNo=number)
    else:
        updateProfile = Profile(user=request.user,middleName=mname,contactNo=number)
        updateProfile.save()
    print('update')

    user = User.objects.filter(id=request.user.id)
    profile = Profile.objects.filter(user=request.user)

    return [
      user,
      profile,
    ]

    print(profile)

  def removeUser(self, user):
    User.objects.filter(id=user.id).delete()

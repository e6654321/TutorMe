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
    
  def updateUser(self, user):
    fname = user.POST.get('fname')
    mname = user.POST.get('mname')
    lname = user.POST.get('lname')
    email = user.POST.get('email')
    number = user.POST.get('number')
    username = user.POST.get('username')
    self.user.objects.filter(
            id=user.user.id
        ).update(first_name=fname,last_name=lname, email=email, username=username)
    
    
    profile = Profile.objects.filter(user=user.user)

    if profile.exists():
        profile.update(middleName=mname,contactNo=number)
    else:
        updateProfile = Profile(user=user.user,middleName=mname,contactNo=number)
        updateProfile.save()
    print('update')

    user = self.user.objects.filter(id=user.user.id)
    profile = Profile.objects.filter(user=user.user)

    print(profile[0])

  def removeUser(self, user):
    self.user.objects.filter(id=user.id).delete()

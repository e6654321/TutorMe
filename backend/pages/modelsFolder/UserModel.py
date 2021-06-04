from backend.pages.models import Profile
from datetime import date

class UserModel():
  firstname = ""
  middlename = ""
  lastname = ""
  gender = ""
  status = ""
  birthdate = date.today()
  email = ""
  contactNo = 0
  username = ""
  street = ""
  brgy = ""
  city = ""
  province = ""
  region = 0

  def getFirstname(self):
    return self.firstname

  def getMiddlename(self):
    return self.middlename

  def getLastname(self):
    return self.lastname

  def getGender(self):
    return self.gender

  def getStatus(self):
    return self.status

  def getBirthdate(self):
    return self.birthdate

  def getEmail(self):
    return self.email

  def getContactNo(self):
    return self.contactNo

  def getUsername(self):
    return self.username

  def getStreet(self):
    return self.street

  def getBrgy(self):
    return self.brgy

  def getCity(self):
    return self.city
    
  def getProvince(self):
    return self.province

  def getRegion(self):
    return self.region

  def setFirstname(self, firstname):
    self.firstname = firstname

  def setMiddlename(self, middlename):
    self.middlename = middlename

  def setLastname(self, lastname):
    self.lastname = lastname

  def setGender(self, gender):
    self.gender = gender

  def setStatus(self, status):
    self.status = status

  def setBirthdate(self, birthdate):
    self.birthdate = birthdate

  def setEmail(self, email):
    self.email = email

  def setContactNo(self, contactNo):
    self.contactNo = contactNo

  def setUsername(self, username):
    self.username = username

  def setStreet(self, street):
    self.street = street

  def setBrgy(self, brgy):
    self.brgy = brgy

  def setCity(self, city):
    self.city = city

  def setProvince(self, province):
    self.province = province

  def setRegion(self, region):
    self.region = region
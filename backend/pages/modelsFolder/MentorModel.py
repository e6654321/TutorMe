from django.db.models import query
from ..views import Mentor

class MentorModel():
    def addMentor(self, achvements, proofs, userID):
        try:
            newMentor = Mentor()
            newMentor.achvemnts=achvements
            newMentor.proofs=proofs
            newMentor.user_identification=userID
            newMentor.save()
            print('saved')
        except Exception as e:
            print(e)
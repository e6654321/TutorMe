from django.db.models import query
from ..views import Mentee

class MenteeModel():

    def addMentee(self, bio, userID):
        try:
            newMentee = Mentee()
            newMentee.bio = bio
            newMentee.user_identification=userID
            newMentee.save()
            print('saved')
        except Exception as e:
            print(e)
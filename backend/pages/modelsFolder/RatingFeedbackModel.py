from django.db import models
from ..views  import Ratings, Comments
class RatingFeedbackModel():
  rating_val = 0
  feedback = ""


  def setRating(rate):
    try:
        rating = Ratings()
        rating.rate = rate
        rating.save()
        return rating
    except Exception as e:
        print(e)
  
  def setFeedback(feedback):
    try:
        review = Comments()
        review.comment = feedback
        review.save()
        return review
    except Exception as e:
        print(e)
  
  def getRating(id):  
   return Ratings.objects.get(id)
  
  def getFeedback(id):
    return Comments.objects.get(id)
  
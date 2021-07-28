
class RatingFeedbackModel():
  rating = 0
  feedback = ""

  def setRating(self, rating):
    self.rating = rating
  
  def setFeedback(self, feedback):
    self.feedback = feedback
  
  def getRating(self):
    return self.rating
  
  def getFeedback(self):
    return self.feedback
  
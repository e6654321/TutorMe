from ..templatesFolder.RatingFeedbackTemplate import RatingFeedbackTemplate
from ..modelsFolder.RatingFeedbackModel import RatingFeedbackModel

class PaymentView():
  ratingFeedbackTemplate = RatingFeedbackTemplate
  ratingFeedbackModel = RatingFeedbackModel

  def setRating(self, rating):
    self.ratingFeedbackModel.setRating(self, rating)
    
  def setFeedback(self, feedback):
    self.ratingFeedbackModel.setFeedback(self, feedback)
    
  def getRating(self):
    return self.ratingFeedbackModel.rating
    
  def getFeedback(self):
    return self.ratingFeedbackModel.feedback
    
  def updateTemplate(self):
    return self.ratingFeedbackTemplate
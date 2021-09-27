from django.shortcuts import redirect
from .CommonUserTemplate import CommonUserTemplate

class RatingFeedbackTemplate():
      def viewReview(self, request):
        return CommonUserTemplate.RatingFeedbackTemplate(self, request)
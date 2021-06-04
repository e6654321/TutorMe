from .CommonUserTemplate import CommonUserTemplate

class GeolocationTemplate():
  def viewGeolocation(self, request):
    return CommonUserTemplate.geolocation(self, request)
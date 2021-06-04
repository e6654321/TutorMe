from ..templatesFolder.GeolocationTemplate import GeolocationTemplate
from ..modelsFolder.GeolocationModel import GeolocationModel

class GeolocationView():
  geolocationTemplate = GeolocationTemplate
  geolocationModel = GeolocationModel

  def schedViaGeolocation(self, ulocation):
    self.geolocationModel.schedViaGeolocation(self, ulocation)
    
  def updateTemplate(self):
    return self.geolocationTemplate
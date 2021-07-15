from ..templatesFolder.ScheduleTemplate import ScheduleTemplate
from ..modelsFolder.ScheduleModel import ScheduleModel


class ScheduleView():
    scheduleTemplate = ScheduleTemplate
    scheduleModel = ScheduleModel

    def enterSubject(self, subject):
        self.scheduleModel.setSubject(self, subject)

    def enterTime(self, sched):
        self.scheduleModel.setTime(self, sched)

    def enterRate(self, rate):
        self.scheduleModel.setRate(self, rate)

    def autoMatch(self):
        self.scheduleTemplate.autoMatch(self)

    def schedViaGeo(self, ulocation):
        self.scheduleModel.schedViaGeo(self, ulocation)

    def viewSched(self):
        self.scheduleModel.reqSched(self)

    def addSched(self):
        self.scheduleModel.addSched(self)

    def cancelSched(self):
        self.scheduleModel.cancelSched(self)

    def pay(self):
        self.scheduleModel.pay(self)

    def addPNotes(self):
        self.scheduleModel.addPNotes(self)

    def editPNotes(self):
        self.scheduleModel.editPNotes(self)

    def updateTemplate(self):
        return self.scheduleTemplate

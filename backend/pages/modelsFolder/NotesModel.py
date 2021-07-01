from django.db.models import query
from ..views  import Notes

class NotesModel():
    notes= Notes()

    def getSpecificNote(nID):
        return Notes.objects.get(notesID=nID)
    
    def addNotes(menteeID, mentorID, subjectID, notesTitle, notes):
        try:
            new_Notes= Notes()
            new_Notes.menteeID=menteeID
            new_Notes.mentorID=mentorID
            new_Notes.subjectID=subjectID
            new_Notes.notesTitle=notesTitle
            new_Notes.notes=notes
            new_Notes.save()
        except Exception as e:
            print(e)
    
    def removeNotes(nID):
        query = Notes.objects.get(pk=nID)
        query.delete()

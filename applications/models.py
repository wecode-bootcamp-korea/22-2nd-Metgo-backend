from django.db.models.base           import Model
from django.db.models                import IntegerField, CharField
from django.db.models.deletion       import CASCADE
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampModel

class Application(TimeStampModel):
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    age     = IntegerField()
    region  = ForeignKey('masters.Region', on_delete=CASCADE)
    career  = CharField(max_length=45)
    gender  = CharField(max_length=20, choices=gender_choice)
    user    = ForeignKey('users.User', on_delete=CASCADE)
    service = ForeignKey('services.Service', on_delete=CASCADE)
    
    class Meta:
        db_table = 'applications'

class ApplicationMaster(Model):
    application = ForeignKey('Application', on_delete=CASCADE)
    master      = ForeignKey('masters.Master', on_delete=CASCADE)

    class Meta:
        db_table = 'application_masters'

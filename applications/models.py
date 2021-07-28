from django.db.models.base           import Model
from django.db.models.deletion       import CASCADE
from django.db.models.enums          import IntegerChoices, TextChoices
from django.db.models.fields         import PositiveIntegerField, CharField
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampModel

class Application(TimeStampModel):

    class Gender(TextChoices):
        MALE   = 'male' 
        FEMALE = 'female'

    class Age(IntegerChoices):
        TEN    = 10
        TWENTY = 20
        THIRTY = 30
        FOURTY = 40
        FIFITY = 50

    class Career(IntegerChoices):
        ZERO               = 0
        FIVE_YEARS         = 5
        TEN_YEARS          = 10
        OVER_FIFTEEN_YEARS = 15

    age     = PositiveIntegerField(choices=Age.choices, null=True)
    region  = ForeignKey('masters.Region', on_delete=CASCADE, null=True)
    career  = PositiveIntegerField(choices=Career.choices, null=True)
    gender  = CharField(max_length=20, choices=Gender.choices, null=True)
    user    = ForeignKey('users.User', on_delete=CASCADE)
    service = ForeignKey('services.Service', on_delete=CASCADE)
    
    class Meta:
        db_table = 'applications'

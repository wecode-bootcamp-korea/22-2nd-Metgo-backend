import re

from django.db.models                import Model
from django.db.models.deletion       import CASCADE

from django.db.models.fields         import BooleanField, CharField, DateField, EmailField, IntegerField, PositiveIntegerField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.enums          import TextChoices 
from core.models import TimeStampModel

EMAIL_REGEX    = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$'
PASSWORD_REGEX = r'^(?_.*[a-z])(?_.*[A-Z])(?_.*[0-9])(?_.*[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=;:,./<>?]{8,20}$'
PHONE_REGEX    = r'^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$'
NAME_REGEX     = r'^[a-zA-Z가-힇]{2,10}$'

class Master(TimeStampModel):

    class Gender(TextChoices):
        MALE   = 'male'
        FEMALE = 'female'
    
    kakao_id      = IntegerField(unique=True)
    certification = BooleanField(null=True)
    business      = BooleanField(null=True)
    introduction  = CharField(max_length=100, null=True)
    description   = CharField(max_length=300, null=True)
    name          = CharField(max_length=45)
    phone         = CharField(max_length=20, unique=True)
    password      = CharField(max_length=200)
    email         = EmailField(unique=True)
    gender        = CharField(max_length=20, choices=Gender.choices)
    birth         = DateField()
    region        = ForeignKey('Region', on_delete=CASCADE)
    profile_image = URLField(max_length=2000, null=True)
    main_service  = ForeignKey('services.Service', on_delete=CASCADE, related_name='services')
    career        = PositiveIntegerField()
    services      = ManyToManyField('services.Service', through='services.MasterService', related_name='service_masters')

    @classmethod
    def validate(cls,data):
        if not re.match(EMAIL_REGEX, data["email"]):
            return False
        if not re.match(PASSWORD_REGEX, data["password"]):
            return False
        if not re.match(PHONE_REGEX, data["phone"]):
            return False
        if not re.match(NAME_REGEX, data["name"]):
            return False
        return True

    class Meta:
        db_table = 'masters'

class Region(Model):
    name = CharField(max_length=100)

    class Meta:
        db_table = 'regions'

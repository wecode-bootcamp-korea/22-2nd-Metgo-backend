import re

from django.db.models                import Model
from django.db.models.deletion       import CASCADE
from django.db.models.fields         import BooleanField, CharField, DateField, EmailField, IntegerField, PositiveIntegerField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.db.models.enums          import TextChoices 

from core.models import TimeStampModel

EMAIL_REGEX    = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=;:,./<>?]{8,20}$'
PHONE_REGEX    = r'^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$'
NAME_REGEX     = r'^[a-zA-Z가-힇]{2,10}$'

class Master(TimeStampModel):
    
    class Gender(TextChoices):
        MALE   = 'male'
        FEMALE = 'female'
    
    kakao_id      = IntegerField(unique=True, null=True)
    certification = BooleanField(null=True)
    business      = BooleanField(null=True)
    introduction  = CharField(max_length=100, null=True)
    description   = CharField(max_length=300, null=True)
    name          = CharField(max_length=45, null=True)
    phone         = CharField(max_length=20, unique=True, null=True)
    password      = CharField(max_length=200)
    email         = EmailField(unique=True)
    gender        = CharField(max_length=20, choices=Gender.choices, null=True)
    birth         = DateField(null=True)
    region        = ForeignKey('Region', on_delete=CASCADE, null=True)
    profile_image = URLField(max_length=2000, null=True)
    main_service  = ForeignKey('services.Service', on_delete=CASCADE, related_name='services', null=True)
    career        = PositiveIntegerField(null=True)
    services      = ManyToManyField('services.Service', through='services.MasterService', related_name='service_masters', null=True)

    @classmethod
    def validate(cls,data):
        if not re.match(EMAIL_REGEX, data["email"]):
            return False
        if not re.match(PASSWORD_REGEX, data["password"]):
            return False
        if not re.match(NAME_REGEX, data["name"]):
            return False
        return True

    class Meta:
        db_table = 'masters'

class UploadedImage(TimeStampModel):
    uploaded_image = URLField()
    master         = ForeignKey('Master', on_delete=CASCADE, related_name='uploaded_images')

    class Meta:
        db_table = 'uploaded_images'


class Region(Model):
    name = CharField(max_length=100)

    class Meta:
        db_table = 'regions'

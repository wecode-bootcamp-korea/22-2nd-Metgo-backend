import re

from django.db.models.enums  import TextChoices
from django.db.models.fields import CharField, DateField, EmailField, IntegerField

from core.models import TimeStampModel

EMAIL_REGEX    = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$'
PASSWORD_REGEX = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=;:,./<>?]{8,20}$'
PHONE_REGEX    = r'^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$'
NAME_REGEX     = r'^[a-zA-Z가-힇]{2,10}$'

class User(TimeStampModel):
    
    class Gender(TextChoices):
        MALE   = 'male'
        FEMALE = 'female'
    
    kakao_id = IntegerField(unique=True)
    name     = CharField(max_length=45)
    password = CharField(max_length=200)
    phone    = CharField(max_length=20, unique=True)
    gender   = CharField(max_length=20, choices=Gender.choices)
    email    = EmailField(unique=True)
    birth    = DateField()
    
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
        db_table = 'users' 
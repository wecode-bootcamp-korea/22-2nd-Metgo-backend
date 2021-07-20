import re

from django.db.models.fields import CharField, DateField, EmailField, IntegerField

from core.models import TimeStampModel

EMAIL_REGEX    = r'^[a-zA-Z0-9]+@[a-zA-Z0-9]+.[a-zA-Z0-9]+$'
PASSWORD_REGEX = r'^(?_.*[a-z])(?_.*[A-Z])(?_.*[0-9])(?_.*[!@#$%^&*()-=_+])[a-zA-Z0-9`~!@#$%^&*()_+-=;:,./<>?]{8,20}$'
PHONE_REGEX    = r'^[0-9]{3}-[0-9]{3,4}-[0-9]{4}$'
NAME_REGEX     = r'^[a-zA-Z가-힇]{2,10}$'

class User(TimeStampModel):
    gender_choice = (
        ('male', 'Male'),
        ('female', 'Female')
    )
    kakao_id = IntegerField()
    name     = CharField(max_length=45)
    phone    = CharField(max_length=20)
    gender   = CharField(max_length=20, choices=gender_choice, null=True)
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

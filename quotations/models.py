from django.db.models.enums          import TextChoices
from django.db.models.fields         import CharField, DecimalField

from django.db.models.deletion       import CASCADE, PROTECT
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampModel

class Quotation(TimeStampModel):

    class Status(TextChoices):
        WAITING  = 'waiting'
        ACCEPTED = 'accepted'
        DENIED   = 'denied'

    user           = ForeignKey('users.User', on_delete=PROTECT)
    price          = DecimalField(max_digits=10, decimal_places=2, null=True)
    status         = CharField(max_length=10, choices=Status.choices, null=True)
    master_service = ForeignKey('services.MasterService', on_delete=CASCADE, related_name='hired_master')

    class Meta:
        db_table = 'quotations'

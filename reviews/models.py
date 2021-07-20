from django.db.models.deletion       import CASCADE
from django.db.models.fields         import PositiveIntegerField, TextField
from django.db.models.fields.related import ForeignKey

from core.models import TimeStampModel

class Review(TimeStampModel):
    content = TextField(max_length=2000, null=True)
    rating  = PositiveIntegerField()
    user    = ForeignKey('users.User', on_delete=CASCADE)
    master  = ForeignKey('masters.Master', on_delete=CASCADE)

    class Meta:
        db_table = 'reviews'

from django.db.models.base           import Model
from django.db.models.deletion       import CASCADE, PROTECT
from django.db.models.fields         import CharField, URLField
from django.db.models.fields.related import ForeignKey, ManyToManyField

class Category(Model):
    name = CharField(max_length=45)

    class Meta:
        db_table = 'categories'

class Service(Model):
    name     = CharField(max_length=45)
    category = ForeignKey('Category', on_delete=PROTECT)
    masters  = ManyToManyField('masters.Master', through='MasterService', related_name='master_services')

    class Meta:
        db_table = 'services'

class MasterService(Model):
    master  = ForeignKey('masters.Master', on_delete=CASCADE)
    service = ForeignKey('Service', on_delete=CASCADE)

    class Meta:
        db_table = 'master_services'

class Image(Model):
    image    = URLField()
    service  = ForeignKey('Service', on_delete=CASCADE)

    class Meta:
        db_table = 'images'

from django.db.models.fields import DateField
from django_seed import Seed
from faker import Faker
import bcrypt
import random

from django.core.management.base import BaseCommand

from users.models import User
from masters.models import Region, Master
from services.models import Service

class Command(BaseCommand):

    help = 'This Command create users'

    def add_arguments(self,parser):
        parser.add_argument(
            '-number', default=1, type=int, help="How many users do you want to create?"
        )

    def handle(self, *args, **options):
        gender_choice = ('male', 'female')
        number = options.get('number')
        seeder = Seed.seeder()
        seeder.add_entity(Master, number, {
            "name" : lambda x : Faker("ko_KR").name(),
            "certification": lambda x : random.randint(0,1),
            "business": lambda x : random.randint(0,1),
            "kakao_id" : lambda x : random.randint(1,100000),
            "password" : lambda x : bcrypt.hashpw( '1234qwer'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "phone" : lambda x : '010'+str(random.randint(1000,9999))+str(random.randint(1000,9999)),
            "gender" : lambda x : random.choice(gender_choice),
            "email" : lambda x : seeder.faker.email() if not User.objects.filter(email = seeder.faker.email()) else ValueError,
            "birth" : lambda x : Faker().date(),
            "region" : lambda x : random.choice(Region.objects.all()),
            "main_service" : lambda x : random.choice(Service.objects.all()),
            "profile_image" : lambda x : None,
            "career" : lambda x : random.randint(0,30),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS({f'{number}users created'}))

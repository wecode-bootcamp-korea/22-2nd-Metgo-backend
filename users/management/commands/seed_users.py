from django.db.models.fields import DateField
from django_seed import Seed
from faker import Faker
import bcrypt
import random

from django.core.management.base import BaseCommand

from users.models import User

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
        seeder.add_entity(User, number, {
            "name" : lambda x : Faker("ko_KR").name(),
            "kakao_id" : lambda x : random.randint(1,100000),
            "password" : lambda x : bcrypt.hashpw( '1234qwer'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            "phone" : lambda x : '010'+str(random.randint(1000,9999))+str(random.randint(1000,9999)),
            "gender" : lambda x : random.choice(gender_choice),
            "email" : lambda x : seeder.faker.email(),
            "birth" : lambda x : Faker().date(),
        })
        seeder.execute()
        self.stdout.write(self.style.SUCCESS({f'{number}users created'}))
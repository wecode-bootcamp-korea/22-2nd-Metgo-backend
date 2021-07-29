import json
import jwt
import datetime

from django.test        import TestCase
from django.test.client import Client

from users.models    import User
from services.models import Service,Category
from masters.models  import Master,Region
from my_settings     import SECRET_KEY,ALGORITHM

class ApplicationTest(TestCase):
    def setUp(self):
        client = Client()
        Category.objects.create(
            id   = 1,
            name = "레슨"
        )
        Service.objects.create(
            id          = 1,
            name        = "보컬 레슨",
            category_id = 1
        )
        User.objects.create(
            id       = 1,
            password = '1234qwer',
            email    = '123456qwer@naver.com',
        )
        Region.objects.create(
            id   = 1,
            name = "강남구"
        )
        Master.objects.create(
            id              = 1,
            name            = '신재',
            password        = '1234qwer',
            email           = '1234qwerasdasd@naver.com',
            main_service_id = 1,
            career          = 10,
            region_id       = 1,
            birth           = '1993-07-11',
            gender          = 'male'
        )

    def tearDown(self):
        Master.objects.all().delete()
        Region.objects.all().delete()
        User.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()

    def test_application_post_success_view(self):
        
        client   = Client()
        application = {
            'user_id'    : 1,
            'age'        : '무관',
            'career'     : 10,
            'region'     : '강남구',
            'service_id' : 1,
            'gender'     : '남'
        }
        
        access_token    = jwt.encode({'id': 1 }, SECRET_KEY, algorithm = ALGORITHM)
        headers = {"HTTP_AUTHORIZATION":access_token}
        
        response = client.post('/applications',json.dumps(application), **headers,content_type='application/json')
        
        self.assertEqual(response.json(),{'message' : 'Success'})
        self.assertEqual(response.status_code, 201)
    
    def test_application_key_error_view(self): 
        client   = Client()
        application = {
            'user_id'    : 1,
            'age'        : '무관',
            'career'     : 20,
            'service_id' : 1,
            'gender'     : '남'
        }
        access_token    = jwt.encode({'id': 1 }, SECRET_KEY, algorithm = ALGORITHM)
        headers = {"HTTP_AUTHORIZATION":access_token}
        response = client.post('/applications', json.dumps(application), **headers, content_type='application/json')

        self.assertEqual(response.json(),{'message' : 'KEY ERROR'})
        self.assertEqual(response.status_code, 404)
import unittest, re, json, jwt, bcrypt
from django.test       import TestCase, Client
from masters.models    import Master, Region, UploadedImage
from services.models   import Category, Service, MasterService
from users.models      import User
from reviews.models    import Review
from quotations.models import Quotation

import unittest, re, json

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from my_settings  import SECRET_KEY, ALGORITHM

class MasterViewTest(TestCase):
    def setUp(self):


        Region.objects.create(
            id   = 1,
            name = '용산구'
        )

        User.objects.create(
            id = 1,
            kakao_id = 1234,
            name = '임유저',
            password = 'Qwer1234!',
            phone = '010-1234-1234',
            gender = 'Female',
            email = 'email@email.com',
            birth = '1990-10-10'
        )

        Category.objects.create(
           id = 1,
            name = '레슨'
        )

        Service.objects.create(
            id = 1,
            name = '골프 레슨',
            category_id = 1
        )
        
        Master.objects.create(
            id                = 1,
            gender            = 'male',
            birth             = '2020-10-10',
            profile_image     = 'image.url',
            name              = 'John',
            main_service_id   = 1,
            introduction      = 'this is introduction',
            region_id         = 1,
            career            = 5,
            certification     = 1,
            business          = 1,
            description       = 'this is description',
        )

        UploadedImage.objects.create(
            id = 1,
            uploaded_image = ['image_1.url', 'image_2.url'],
            master_id = 1
        )

        MasterService.objects.create(
            id = 1,
            master_id = 1,
            service_id = 1
        )

        Quotation.objects.create(
            id = 1,
            user_id = 1,
            price = 1000,
            status = 'accepted',
            master_service_id = 1,
        )

        Review.objects.create(
            id = 1,
            content = 'this is content',
            rating = 4,
            master_id = 1,
            service_id = 1,
            user_id = 1
        )

        
    def tearDown(self):
        Review.objects.all().delete(),
        Quotation.objects.all().delete()
        MasterService.objects.all().delete(),
        UploadedImage.objects.all().delete(),
        Master.objects.all().delete(),
        Service.objects.all().delete(),
        Category.objects.all().delete(),
        User.objects.all().delete(),
        Region.objects.all().delete(),

    def test_master_id_exists(self):
        client = Client()
        response = client.get('/masters/2')
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : 'DOES_NOT_EXISTS'}
        )

    def test_masterview(self):
        client   = Client()
        response = client.get('/masters/1')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'data': [
                {'gender'         : 'male',
                 'birth'          : '2020-10-10',
                 'profile_image'  : 'image.url',
                 'name'           : 'John',
                 'main_service'   : '골프 레슨',
                 'average_rating' : 4.0,
                 'review_counts'  : 1,
                 'introduction'   : 'this is introduction',
                 'region'         : '용산구',
                 'career'         : 5,
                 'certification'  : True,
                 'business'       : True,
                 'description'    : 'this is description',
                 'hired'          : 1,
                 'uploaded_image' : ["['image_1.url', 'image_2.url']"]}
            ]}
        )
 


class MasterSignupTest(TestCase):
    def setUp(self):
        Master.objects.create(
            name        = '최준영임',
            email       = 'wewewe@naver.com',
            password    = 'qwerQWER1234!'
        )

    def tearDown(self):
        Master.objects.all().delete()

    def test_master_signup_success(self):
        client = Client()
        master = {
            'name'      : '최준영입니다',
            'email'     : 'wweweweweweww@naver.com',
            'password'  : 'qwerQWER1234!'
        }

        response = client.post("/masters/signup", json.dumps(master), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            "message":"SUCCESS"
            })

    def test_master_signup_exists_email(self):
        client  = Client()
        master    = {
            'name' : '최준영임',
            'email' : 'wewewe@naver.com',
            'password' : 'qwerQWER1234!'
        }

        response = client.post("/masters/signup", json.dumps(master), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message":"ACCOUNT_ALREADY_EXIST"
            })

    def test_master_signup_key_error(self):
        client  = Client()
        master    = {
            'first_name'    : '준영초이',
            'email'         : 'showmethr23@hotmail.com',
            'password'      : 'qwerQWER1234!'
        }

        response = client.post("/masters/signup", json.dumps(master), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message':'KEY_ERROR'
            })

    def test_master_signup_valitation_error(self):
        client  = Client()
        master    = {
            'name'      : 'junyeongchoiiiii',
            'email'     : 'shwwwehotmail.com',
            'password'  : 'qwerQWER1234'
        }

        response = client.post("/masters/signup", json.dumps(master), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            'message':'VALIDATION_ERROR'
            })

class MasterSigninTest(TestCase):
    def setUp(self):
        password = 'qwerQWER1234!'

        Master.objects.create(
            id          = 1,
            name        = '최준영',
            email       = 'wework@naver.com',
            password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        access_token = jwt.encode({'master_id':1}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        Master.objects.all().delete()

    def test_teset_est_et(self):

        client = Client()

        master= {
            'email'   :'wework@naver.com',
            'password':'qwerQWER1234!'
        }

        response     = client.post('/masters/signin', json.dumps(master), content_type='application/json')

        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message': 'SUCCESS',
                'access_token'  : access_token
            }
        )

    def test_master_password_error(self):

        client = Client()

        master = {
            'email':'wework@naver.com',
            'password':'qwerQWER11!'
        }

        response     = client.post('/masters/signin', json.dumps(master), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message': 'PASSWORD_ERROR',
            }
        )

    def test_master_email_not_exist(self):

        client = Client()

        master = {
            'email':'letsgoshow',
            'password':'qwerQWER1234!'
        }

        response = client.post('/masters/signin', json.dumps(master), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message":"USER_NOT_EXIST"
        })

class MasterKakaoSigninTest(TestCase):
    def setUp(self):
        Master.objects.create(
            id          = 1,
            kakao_id    = 1234567,
            email       = 'jungzkxm@daum.net',
            name        = '성정준',
            gender      = 'male'
        )

    def tearDown(self):
        Master.objects.all().delete()

    @patch('masters.views.requests')
    def test_master_kakao_signin_success(self, mocked_requests):

        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'id':1234567,
                    'connected_at'  : '2021-07-21T04:00:48Z',
                    'properties'    :{
                        'nickname'  : '임한병'
                    },
                    'kakao_account' :{
                        'profile_nickname_needs_agreement' : False,
                        'profile' : {
                            'nickname'                  : '임한별',
                            'has_email'                 : True,
                            'email_needs_agreement'     : False,
                            'is_email_valid'            : True,
                            'is_email_verified'         : True,
                            'email'                     : 'swnwnwnwn@daum.net',
                            'has_age_range'             : True,
                            'age_range_needs_agreement' : False,
                            'age_range'                 : '20~29',
                            'has_gender'                : True,
                            'gender_needs_agreement'    : False,
                            'gender'                    : 'male',
                        },
                    }
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse())
        headers              = {"HTTP_Authorization":"kakao_token"}
        response             = client.post("/masters/kakao/signin", **headers)

        access_token         = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message'           : 'SUCCESS',
                'access_token'      : access_token
            }
        )

    @patch('masters.views.requests')
    def test_master_kakao_signin_success(self, mocked_requests):

        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    'sayhoid':1234567,
                    'connected_at'  : '2021-07-21T04:00:48Z',
                    'properties'    :{
                        'nickname'  : '임한병'
                    },
                    'kakao_account' :{
                        'profile_nickname_needs_agreement' : False,
                        'profile' : {
                            'nickname'                  : '임한별',
                            'has_email'                 : True,
                            'email_needs_agreement'     : False,
                            'is_email_valid'            : True,
                            'is_email_verified'         : True,
                            'email'                     : 'swnwnwnwn@daum.net',
                            'has_age_range'             : True,
                            'age_range_needs_agreement' : False,
                            'age_range'                 : '20~29',
                            'has_gender'                : True,
                            'gender_needs_agreement'    : False,
                            'gender'                    : 'male',
                        },
                    }
                }

        mocked_requests.post = MagicMock(return_value = MockedResponse())
        headers              = {"HTTP_Authorization":"kakao_token"}
        response             = client.post("/masters/kakao/signin", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message'           : 'INVALID_KEY',
            }
        )

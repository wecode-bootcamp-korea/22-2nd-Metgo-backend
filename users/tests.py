import unittest, re, json, jwt, bcrypt

from django.test   import TestCase, Client
from unittest.mock import patch, MagicMock

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

class UserSignupTest(TestCase):
    def setUp(self):
        User.objects.create(
            name        = '최준영',
            email       = 'wewe@naver.com',
            password    = 'qwerQWER1234!'
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_signup_success(self):
        client = Client()
        user = {
            'name'      : '최준영',
            'email'     : 'weweeeeee@naver.com',
            'password'  : 'qwerQWER1234!'
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'message':'SUCCESS'
            })

    def test_user_signup_exists_email(self):
        client  = Client()
        user    = {
            'name' : '최준영',
            'email' : 'wewe@naver.com',
            'password' : 'qwerQWER1234!'
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),{
            "message":"ACCOUNT_ALREADY_EXIST"
            })

    def test_user_signup_key_error(self):
        client  = Client()
        user    = {
            'first_name'    : '준영초이',
            'email'         : 'showmethr23@hotmail.com',
            'password'      : 'qwerQWER1234!'
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            'message':'KEY_ERROR'
            })

    def test_user_signup_valitation_error(self):
        client  = Client()
        user    = {
            'name'      : 'junyeongchoiiiii',
            'email'     : 'shwwwehotmail.com',
            'password'  : 'qwerQWER1234'
        }

        response = client.post("/users/signup", json.dumps(user), content_type="application/json")
        
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {
            'message':'VALIDATION_ERROR'
            })

class UserSigninTest(TestCase):
    def setUp(self):
        password = 'qwerQWER1234!'

        User.objects.create(
            id          = 1,
            name        = '최준영',
            email       = 'wework@naver.com',
            password    = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

        access_token = jwt.encode({'user_id':1}, SECRET_KEY, ALGORITHM)

    def tearDown(self):
        User.objects.all().delete()

    def test_teset_est_et(self):

        client = Client()

        user= {
            'email'   :'wework@naver.com',
            'password':'qwerQWER1234!'
        }

        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        access_token = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 
            {
                'message': 'SUCCESS',
                'access_token'  : access_token
            }
        )

    def test_user_password_error(self):

        client = Client()

        user = {
            'email':'wework@naver.com',
            'password':'qwerQWER11!'
        }

        response     = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 
            {
                'message': 'PASSWORD_ERROR',
            }
        )

    def test_user_email_not_exist(self):

        client = Client()

        user = {
            'email':'letsgoshow',
            'password':'qwerQWER1234!'
        }

        response = client.post('/users/signin', json.dumps(user), content_type='application/json')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "message":"USER_NOT_EXIST"
        })

class UserKakaoSigninTest(TestCase):
    def setUp(self):
        User.objects.create(
            id          = 1,
            kakao_id    = 1234567,
            email       = 'jungzkxm@daum.net',
            name        = '성정준',
            gender      = 'male'
        )

    def tearDown(self):
        User.objects.all().delete()

    @patch('users.views.requests')
    def test_user_kakao_signin_success(self, mocked_requests):

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
        response             = client.post("/users/kakao/signin", **headers)

        access_token         = response.json()['access_token']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {
                'message'           : 'SUCCESS',
                'access_token'      : access_token
            }
        )

    @patch('users.views.requests')
    def test_user_kakao_signin_success(self, mocked_requests):

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
        response             = client.post("/users/kakao/signin", **headers)
        
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                'message'           : 'INVALID_KEY',
            }
        )

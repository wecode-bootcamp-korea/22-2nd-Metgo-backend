import unittest, re, json

from django.test  import TestCase, Client

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
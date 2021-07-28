import unittest, re, json

from django.test import TestCase, Client

from masters.models import Master

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
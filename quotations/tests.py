import json
import jwt

from django.test         import TestCase
from django.test.client  import Client

from applications.models import Application
from users.models        import User
from services.models     import Service,Category,MasterService
from masters.models      import Master,Region
from quotations.models   import Quotation
from my_settings         import SECRET_KEY,ALGORITHM

class QuotationTest(TestCase):
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
            name     = '신재',
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
            career          = 10
        )
        MasterService.objects.create(
            id         =1,
            master_id  =1,
            service_id =1
        )
        Application.objects.create(
            id         = 1,
            user_id    = 1,
            service_id = 1
        )
        Quotation.objects.create(
            id                = 1,
            user_id           = 1,
            master_service_id = 1,
            status            = 0
        )
    
    def tearDown(self):
        Quotation.objects.all().delete()
        Master.objects.all().delete()
        Region.objects.all().delete()
        User.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()

    def test_quotation_post_success_view(self):
        client    = Client()
        quotation = {
            "id"                : 1,
            "user_id"           : 1,
            "master_service_id" : 1,
            "status"            : "waiting",
        }
        
        access_token    = jwt.encode({ 'id': 1 }, SECRET_KEY, algorithm = ALGORITHM)
        headers         = { "HTTP_AUTHORIZATION" : access_token }
        
        response        = client.post('/quotations', json.dumps(quotation), **headers, content_type='application/json')
        
        self.assertEqual(response.json(),{ 'message' : 'Success' })
        self.assertEqual(response.status_code, 201)
    
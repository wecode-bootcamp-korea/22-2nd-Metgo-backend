from django.test         import TestCase, Client

from users.models        import User
from services.models     import Service,Category, Image, MasterService
from masters.models      import Master
from applications.models import Application
from reviews.models      import Review

class CategoryTest(TestCase):
    def setUp(self):
        client = Client()
        Category.objects.create(
            id   = 1,
            name = "레슨"
        )
        Category.objects.create(
            id   = 2,
            name = "알바"
        )
        Category.objects.create(
            id   = 3,
            name = "체육"
        )

    def tearDown(self):
        Category.objects.all().delete()

    def test_category_get_view(self):
        client   = Client()
        response = client.get('/categories')

        self.assertEqual(response.json(),
            {
                'categories' : [
                    {
                        "id"   : 1,
                        "name" : "레슨"
                    },
                    {
                        "id"   : 2,
                        "name" : "알바"
                    },
                    {
                        "id"   : 3,
                        "name" : "체육"
                    }
                    
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class ServicesTest(TestCase):
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
        Service.objects.create(
            id          = 2,
            name        = "피아노 레슨",
            category_id = 1
        )
        Image.objects.create(
            id          = 1,
            image       = "http://1233455.jpg",
            service_id  = 1
        )
        Image.objects.create(
            id          = 2,
            image       = "http://1233455.jpg",
            service_id  = 2
        )

    def tearDown(self):
        Image.objects.all().delete()
        Service.objects.all().delete()
        Category.objects.all().delete()

    def test_services_get_view(self):
        client   = Client()
        response = client.get('/categories/1')
        
        self.assertEqual(response.json(),
            {
                'services' : [
                    {
                        "id"    : 1,
                        "name"  : "보컬 레슨",
                        "image" : "http://1233455.jpg"
                    },
                    {
                        "id"    : 2,
                        "name"  : "피아노 레슨",
                        "image" : "http://1233455.jpg"
                    }
                ]
            }
        )
        self.assertEqual(response.status_code, 200)

class ServiceTest(TestCase):
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
        User.objects.create(
            id       = 2,
            password = '1234qwer',
            email    = '1234567qwer@naver.com',
        )
        
        Master.objects.create(
            id              = 1,
            password        = '1234qwer',
            email           = '1234qwerasdasd@naver.com',
            main_service_id = 1,
            career          = 5,
        )
        
        Master.objects.create(
            id              = 2,
            password        = '1234qwer',
            email           = '12344qwerfasd@naver.com',
            main_service_id = 1,
            career          = 5,
        )
        
        MasterService.objects.create(
            master_id  = 1,
            service_id = 1
        )
        MasterService.objects.create(
            master_id  = 2,
            service_id = 1
        )

        Application.objects.create(
            id         = 1,
            user_id    = 1,
            service_id = 1
        )
        
        Application.objects.create(
            id         = 2,
            user_id    = 2,
            service_id = 1
        )
        Review.objects.create(
            rating     = 4.0,
            user_id    = 1,
            master_id  = 1,
            service_id = 1
        )
        Review.objects.create(
            rating     = 2.0,
            user_id    = 2,
            master_id  = 2,
            service_id = 1
        )

    def tearDown(self):
        Service.objects.all().delete()
        User.objects.all().delete()
        Application.objects.all().delete()
        Category.objects.all().delete()
        Review.objects.all().delete()
        Master.objects.all().delete()
        MasterService.objects.all().delete()

    def test_service_get_view(self):
        client   = Client()
        response = client.get('/services/1')
        self.assertEqual(response.json(),
            {
                'results' : [
                    {
                        "service_id"   : 1,
                        "name"         : "보컬 레슨",
                        "rating"       : 3.0,
                        "masters"      : 2,
                        "applications" : 2,
                        "reviews"      : 2,
                    }

                ]
            }
        )
        self.assertEqual(response.status_code, 200)

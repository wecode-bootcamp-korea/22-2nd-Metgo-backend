from django.utils import timezone
from django.test       import TestCase, Client
from masters.models    import Master, Region, UploadedImage
from services.models   import Category, Service, MasterService
from users.models      import User
from reviews.models    import Review
from quotations.models import Quotation

class MasterReviewTest(TestCase):
    def setUp(self):

        Region.objects.create(
            id   = 1,
            name = '용산구'
        )

        User.objects.create(
            id       = 1,
            kakao_id = 1234,
            name     = '임유저',
            password = 'Qwer1234!',
            phone    = '010-1234-1234',
            gender   = 'Female',
            email    = 'email@email.com',
            birth    = '1990-10-10'
        )

        Category.objects.create(
           id    = 1,
            name = '레슨'
        )

        Service.objects.create(
            id          = 1,
            name        = '골프 레슨',
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
            id             = 1,
            uploaded_image = ['image_1.url', 'image_2.url'],
            master_id      = 1
        )

        MasterService.objects.create(
            id         = 1,
            master_id  = 1,
            service_id = 1
        )

        Quotation.objects.create(
            id                = 1,
            user_id           = 1,
            price             = 1000,
            status            = 'accepted',
            master_service_id = 1,
        )

        Review.objects.create(
            id         = 1,
            content    = 'this is content',
            rating     = 4,
            master_id  = 1,
            service_id = 1,
            user_id    = 1,
            created_at = '2021-07-29T11:56:50:000Z'
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
        Region.objects.all().delete()

    def test_master_id_exists(self):
        client   = Client()
        response = client.get('/reviews/2')
        print(response.json())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {'message' : 'DOES_NOT_EXISTS'}
        )

    def test_master_review(self):
        client   = Client()
        response = client.get('/reviews/1')
        print(response.json())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {'results': [ {
                'name'       : '임유저',
                'rating'     : 4,
                'created_at' : '2021-07-29T11:56:50:000Z',
                'content'    : 'this is content',
            }]}
        )

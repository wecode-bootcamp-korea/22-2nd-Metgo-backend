from django.test import TestCase, Client #테스트를 위한 클래스 임포트


class JustTest(TestCase):
    def test_just_get_view(self):
        client   = Client() #client는 requests나 httpie가 일하는 방식과 같이 동작하는 객체.
		response = client.get('/just')

				#현재 우리는 localhost로서가 아닌 기준 경로로부터 실행 
        self.assertEqual(response.status_code, 200)

				#응답 코드를 비교 
        self.assertEqual(response.json(), {
            "message": "Just Do Python with >Wecode"
        })
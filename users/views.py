import json, bcrypt, jwt, datetime, requests

from django.views import View
from django.http  import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

class UserSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not User.validate(data):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=401)

            email           = data["email"]
            password        = data["password"]
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            if User.objects.filter(email=email).exists():
                return JsonResponse({"message":"ACCOUNT_ALREADY_EXIST"}, status=400)

            User.objects.create(
                name            = data["name"],
                password        = hashed_password.decode(),
                email           = email,
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class UserSigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email       = data["email"]
            password    = data["password"]
            user        = User.objects.get(email=email)

            if not bcrypt.checkpw(password.encode(), user.password.encode()):
                return JsonResponse({"message":"PASSWORD_ERROR"}, status=400)

            exp = datetime.datetime.now() + datetime.timedelta(hours=1)

            access_token    = jwt.encode(
                payload     ={'id':user.id, 'exp':exp},
                key         = SECRET_KEY,
                algorithm   = ALGORITHM
            )
            return JsonResponse({"message":"SUCCESS", "access_token":access_token}, status=200)

        except jwt.ExpiredSignatureError:
            return JsonResponse({"message":"EXPIRED_TOKEN"}, status=400)

        except User.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)

class UserKakaoSigninView(View):
    def post(self, request):
        try:
            kakao_access_token    = request.headers.get('Authorization')
            
            profile         = requests.post(
                'https://kapi.kakao.com/v2/user/me', 
                headers     = {'Authorization': f"Bearer {kakao_access_token}"}
            )

            kakao_profile   = profile.json()
            
            user, is_created = User.objects.get_or_create(kakao_id=kakao_profile['id'])
            
            if is_created:
                user.name        = kakao_profile['kakao_account']['profile']['nickname']
                user.gender      = kakao_profile['kakao_account']['gender']
                user.email       = kakao_profile['kakao_account']['email']
                user.save()
            
            access_token = jwt.encode({'id': user.id}, SECRET_KEY, ALGORITHM)
            
            return JsonResponse({'message':'SUCCESS','access_token' : access_token}, status = 200)
        
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)
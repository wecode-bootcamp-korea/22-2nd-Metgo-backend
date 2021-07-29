import json, bcrypt, jwt, datetime, requests

from django.views import View
from django.http  import JsonResponse

from my_settings    import SECRET_KEY, ALGORITHM
from masters.models import Master
from django.views                import View
from django.http                 import JsonResponse
from django.db.models.aggregates import Avg
from masters.models              import Master

from quotations.models import Quotation
from services.models import MasterService

from masters.models import Region
from core.views     import master_signin_check, AWSAPI
from my_settings    import BUCKET, AWS_SECRET_ACCESS_KEY, AWS_ACCESS_KEY_ID



class MasterSignupView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            
            if not Master.validate(data):
                return JsonResponse({"message":"VALIDATION_ERROR"}, status=401) 

            email           = data["email"]
            password        = data["password"]
            hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            if Master.objects.filter(email=email).exists():
                return JsonResponse({"message":"ACCOUNT_ALREADY_EXIST"}, status=400)

            Master.objects.create(
                name            = data["name"],
                password        = hashed_password.decode(),
                email           = email,
            )
            return JsonResponse({"message":"SUCCESS"}, status=201)
            
        except KeyError:
            return JsonResponse({"message":"KEY_ERROR"}, status=400)

class MasterSigninView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            email       = data["email"]
            password    = data["password"]
            user        = Master.objects.get(email=email)

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

        except Master.DoesNotExist:
            return JsonResponse({"message":"USER_NOT_EXIST"}, status=400)

class MasterKakaoSigninView(View):
    def post(self, request):
        try:
            kakao_access_token    = request.headers.get('Authorization')

            profile         = requests.post(
                'https://kapi.kakao.com/v2/user/me', 
                headers     = {'Authorization': f"Bearer {kakao_access_token}"}
            )

            kakao_profile   = profile.json()

            master, is_created = Master.objects.get_or_create(kakao_id=kakao_profile['id'])

            if is_created:
                master.name        = kakao_profile['kakao_account']['profile']['nickname']
                master.gender      = kakao_profile['kakao_account']['gender']
                master.email       = kakao_profile['kakao_account']['email']
                master.save()

            access_token = jwt.encode({'id': master.id}, SECRET_KEY, ALGORITHM)
            return JsonResponse({'message':'SUCCESS','access_token' : access_token}, status = 200)
            
        except KeyError:
            return JsonResponse({'message': 'INVALID_KEY'}, status = 400)

class MasterView(View):
    def get(self, request, master_id):
        try:
            if not Master.objects.filter(id=master_id).exists():
                return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=400)
            
            master      = Master.objects.get(id=master_id)
            review      = master.review_set.filter(master_id=master.id)
            quotation   = Quotation.objects.filter(master_service_id=MasterService.objects.get(master=master))
            user_rating = (round(review.aggregate(average=Avg('rating'))['average'], 1))
            results = [
                {
                    'gender'         : master.gender,
                    'birth'          : master.birth,
                    'profile_image'  : master.profile_image,
                    'name'           : master.name,
                    'main_service'   : master.main_service.name,
                    'average_rating' : user_rating,
                    'review_counts'  : review.count(),
                    'introduction'   : master.introduction,
                    'region'         : master.region.name,
                    'career'         : master.career,
                    'certification'  : master.certification,
                    'business'       : master.business,
                    'description'    : master.description,
                    'hired'          : quotation.filter(status='accepted').count(),
                    'uploaded_image' : [image.uploaded_image for image in master.uploaded_images.all()]
                }
            ]

            return JsonResponse({'data':results}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
        except TypeError:
            return JsonResponse({'message':'TYPE_ERROR'}, status=400)
        except ValueError:
            return JsonResponse({'message':'VALUE_ERROR'}, status=400)

    @master_signin_check
    def patch(self, request):
        data   = json.loads(request.body)
        master = request.master

        master.name          = data.get("name", master.name)
        master.introduction  = data.get("introduction", master.introduction)
        master.career        = data.get("career", master.career)
        master.business      = data.get("business", master.business)
        master.certification = data.get("certification", master.certification)
        master.description   = data.get("description", master.description)
        master.region        = Region.objects.get(name=data.get("region", master.region.name))
        master.save()

        return JsonResponse({'message':'UPDATED'}, status=200) 

    @master_signin_check
    def post(self, request):
        master                = request.master
        master.uploading_file = request.FILES.get('profile_image')
        aws                   = AWSAPI(AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, BUCKET)

        master.profile_image  = aws.upload_file(master.uploading_file)
        master.save()

        return JsonResponse({'message':'SUCCESS'}, status=200)

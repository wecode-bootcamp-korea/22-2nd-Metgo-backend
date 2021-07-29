import jwt

from django.http import JsonResponse
from my_settings import SECRET_KEY, ALGORITHM

from users.models   import User
from masters.models import Master

def user_signin_check(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization')
            payload         = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            user            = User.objects.get(id=payload["id"])
            request.user    = user
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)

    return wrapper

def master_signin_check(func):
    def wrapper(self,request, *args, **kwargs):
        try:
            access_token    = request.headers.get('Authorization')
            payload         = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
            master          = Master.objects.get(id=payload["id"])
            request.master  = master
            return func(self, request, *args, **kwargs)

        except jwt.DecodeError:
            return JsonResponse({"message":"DECODE_ERROR"}, status=400)

import jwt
import boto3
import uuid

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

    return wrapper

class AWSAPI:
    def __init__(self, aws_access_key, aws_secret_key, bucket):
        self.bucket      = bucket
        self.storage_url = 'https://' + bucket + '.s3.ap-northeast-2.amazonaws.com/'
        self.client      = boto3.client(
            's3',
            aws_access_key_id     = aws_access_key,
            aws_secret_access_key = aws_secret_key
        )
    def upload_file(self, file):
        filename = uuid.uuid4().hex
        self.client.upload_fileobj(
            file,
            self.bucket,
            filename,
            ExtraArgs = {
                'ContentType': file.content_type
            }
        )
        return self.storage_url + filename

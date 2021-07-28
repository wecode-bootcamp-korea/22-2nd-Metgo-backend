import json, bcrypt

from django.views import View
from django.http  import JsonResponse

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
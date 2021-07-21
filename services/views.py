import json

from django.core      import exceptions
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q
from django.db.utils  import DataError

from services.models import Service, Category

class MainView(View):
    def get(self, request, category_name):
        services = Service.objects.filter(category__name=category_name)
        results = [{
            "name" : service.name,
            "image" : service.image_set.all()[0].image,
        }for service in services]

        return JsonResponse({'results': results}, status=200)

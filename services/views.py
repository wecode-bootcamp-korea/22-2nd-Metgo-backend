import json

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import aggregates, Avg

from services.models     import Service, Category, MasterService
from reviews.models      import Review
from applications.models import Application
from masters.models      import Master

class CategoryView(View):
    def get(self, request):
        categories = Category.objects.all()
        category   = [{
            "id"   : category.id,
            "name" : category.name
        } for category in categories]
        
        return JsonResponse({'categories': category}, status=200) 

class ServiceView(View):
    def get(self, request, category_id):
        services = Service.objects.filter(category_id=category_id)
        service  = [{
            "id"    : service.id,
            "name"  : service.name,
            "image" : service.image_set.all()[0].image,
        } for service in services]

        return JsonResponse({'services': service}, status=200)

class ServiceDetailView(View):
    def get(self, request, service_id):
        service = Service.objects.get(id=service_id)
        reviews = service.service_reviews.all()
        rating = reviews.aggregate(Avg("rating"))
        results = [{
            "service_id"   : service.id,
            "name"         : service.name,
            "rating"       : rating["rating__avg"],
            "활동 고수"      : service.service_masters.all().count(),
            "누적 요청서"     : service.application_set.all().count(),
            "리뷰 수"        : reviews.count(),
        }]

        return JsonResponse({'results': results}, status=200)
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

        return JsonResponse({'services' : service}, status=200)

class ServiceDetailView(View):
    def get(self, request, service_id):
        if not Service.objects.get(id=service_id).exists():
            return JsonResponse({'message' : 'Not Found page'}, status=404)

        service = Service.objects.get(id=service_id)
        reviews = service.service_reviews.all()
        rating  = reviews.aggregate(average=Avg("rating"))
        results = [{
            "service_id"   : service.id,
            "name"         : service.name,
            "rating"       : rating.average,
            "masters"      : service.service_masters.all().count(),
            "applications" : service.application_set.all().count(),
            "reviews"      : reviews.count(),
        }]

        return JsonResponse({'results' : results}, status=200)
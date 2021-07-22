import json

from django.http         import JsonResponse
from django.views        import View
from django.db.models    import aggregates, Avg

from services.models     import Service, Category, MasterService
from reviews.models      import Review
from applications.models import Application

class ServiceView(View):
    def get(self, request, category_id):
        categories = Category.objects.all()
        category   = [{
            "id"   : category.id,
            "name" : category.name
        } for category in categories]

        services = Service.objects.filter(category_id=category_id)
        service  = [{
            "id"    : service.id,
            "name"  : service.name,
            "image" : service.image_set.all()[0].image,
        } for service in services]

        return JsonResponse({'categories': category, 'services': service}, status=200) 

class ServiceDetailView(View):
    def get(self, request, service_id):

        service = Service.objects.get(id=service_id)
        reviews = Review.objects.select_related("master").filter(master__services=service)
        rating = reviews.aggregate(Avg("rating"))
        results = [{
            "service_id"   : service.id,
            "name"         : service.name,
            "rating"       : rating["rating__avg"],
            "masters"      : MasterService.objects.filter(service=service).count(),
            "applications" : Application.objects.filter(service=service).count(),
            "reviews"      : reviews.count(),
        }]

        return JsonResponse({'results': results}, status=200)
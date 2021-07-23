import json
import datetime
from dateutil.relativedelta import relativedelta

from django.core      import exceptions
from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, aggregates, Avg
from django.db.utils  import DataError

from masters.models import Master,Region
from services.models import Service
from applications.models import Application, ApplicationMaster
from reviews.models import Review

class ApplicationView(View):
    def post(self,request):
        try:
            data    = json.loads(request.body)
            user    = data["user_id"]
            age     = data["age"]
            career  = data["carrer"]
            gender  = data["gender"]
            region  = Region.objects.get(name=data["region"])
            service = Service.objects.get(id=data["service_id"])
            
            today = datetime.date.today()
            birth = today - relativedelta(year = today.year-age)

            q = Q()
            q = Q()
            q &= Q(main_service = service)
            q &= Q(gender=gender)
            q &= Q(region= region)
            masters = Master.objects.filter(q)
            print(q)
            print(len(masters))
            if masters:
                if age !=50:
                    q &= Q(birth__lte = birth)&Q(birth__gt = birth-relativedelta(year= birth.year-10))
                if age ==50:
                    q &= Q(birth__lte = birth)
                # if Master.objects.filter(q):
                    
            print('q',q)
            print('===================================0===================================')
            if masters:
                if career != 15:
                    q &= Q(career__gte=career)&Q(career__lt=career+5)
                if career == 15:
                    q &= Q(career__gte=career)
                masters = Master.objects.filter(q)
            print('q',q)
            print('===================================1===================================')
            masters = Master.objects.filter(q)
            print(masters)
            print('=========================================2==================================')
            
            if not masters:
                return JsonResponse({'message' : '조건에 맞는 고수가 없습니다'}, status = 201)

            user_application = Application.objects.update_or_create(
                age = age,
                career = career,
                gender = gender,
                region = region,
                service = service,
                user_id = user
            )            

            for master in masters:
                ApplicationMaster.objects.create(
                    application = user_application,
                    master = master
                )
                
            return JsonResponse({'message' : 'Success'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status = 404)

class MasterMatchingView(View):
    def get(self, request, service_id):
        user = request.GET.get('user_id','')
        service = Service.objects.get(id=service_id)
        application = Application.objects.filter(service=service).get(user_id=user)
        reviews = Review.objects.select_related("master")
        results = [{
                "image" : application.master.profile_image,
                "name" : application.master.name,
                "introduction" : application.master.introduction,
                "rating" : reviews.filter(master=application.master).aggregate(Avg("rating"))["rating__avg"],
                "review" : reviews.filter(master=application.master).count()
            } for application in ApplicationMaster.objects.select_related('master').filter(application=application)]

        return JsonResponse({'results' : results}, status = 200)
        
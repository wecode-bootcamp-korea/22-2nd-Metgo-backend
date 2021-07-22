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
        data = json.loads(request.body)
        age = data["age"]
        career = data["carrer"]
        gender = data["gender"]
        region = Region.objects.get(name=data["region"])
        service = Service.objects.get(name=data["service"])
        user = data["user"]
        
        user_application = Application.objects.create(
            age = age,
            career = career,
            gender = gender,
            region = region,
            service = service,
            user_id = user
        )

        today = datetime.date.today()
        birth = today - relativedelta(year = today.year-age)

        q = Q()
        q &= Q(main_service = service)
        q &= Q(gender=gender)
        q &= Q(region= region)

        if age !=50:
            q &= Q(birth__lte = birth)&Q(birth__gt = birth-relativedelta(year= birth.year-10))
        if age ==50:
            q &= Q(birth__lte = birth)
        
        if career != 15:
            q &= Q(career__gte=career)&Q(career__lt=career+5)
        if career == 15:
            q &= Q(career__gte=career)

        masters = Master.objects.filter(q)
        masters.save()
        Review.objects.all().aggregate(Avg("rating"))
        reviews = Review.objects.select_related("masters")

        results = []
        
        for master in masters:
            ApplicationMaster.objects.create(
                applicaiton = user_application,
                master = master
            )
            # sort rating
            results.append({
                "image" : master.profile_image,
                "name" : master.name,
                "introduction" : master.introduction,
                "rating" : reviews.filter(master=master).aggregate(Avg("rating")),
                "review" : reviews.filter(master=master).count()
            })
            
        return JsonResponse({'message' : results}, status = 201)


import json
import datetime
from dateutil.relativedelta import relativedelta

from django.core            import exceptions
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, aggregates, Avg
from django.db.utils        import DataError

from users.models           import User
from masters.models         import Master,Region
from services.models        import Service
from applications.models    import Application, ApplicationMaster
from reviews.models         import Review

class ApplicationView(View):
    def post(self,request):
        try:
            data    = json.loads(request.body)
            user    = User.objects.get(id = data["user_id"])
            age     = data["age"] 
            career  = data["career"]
            region  = Region.objects.get(name = data["region"])
            service = Service.objects.get(id  = data["service_id"])

            gender_choice = {"남" : "male", "여" : "female", "무관" : None}
            gender        = gender_choice[data["gender"]]
            
            today = datetime.date.today()
            birth = today - relativedelta(year = today.year-age)
            
            q  = Q()
            q &= Q(main_service = service)
            
            if gender:
                q &= Q(gender = gender)
            
            if age != '무관':
                if age != 50:
                    q  &= Q(birth__lte = birth)&Q(birth__gt = birth-relativedelta(year= birth.year-10))
                if age == 50:
                    q  &= Q(birth__lte = birth)

            if career != 15:
                q &= Q(career__gte = career)&Q(career__lt = career+5)
            if career == 15:
                q &= Q(career__gte = career)
            
            masters = Master.objects.filter(Q)
            
            if not masters:
                return JsonResponse({'message' : 'Does not matching masters'}, status = 201)

            user_application, created = Application.objects.update_or_create(
                service  = service,
                user     = user,
                defaults = {"age"     : age,
                            "career"  : career,
                            "gender"  : gender,
                            "region"  : region}
            )
            if not created:
                ApplicationMaster.objects.filter(application=user_application).delete()
            
            for master in masters:
                ApplicationMaster.objects.create(
                    application = user_application,
                    master      = master,
                )
                
            return JsonResponse({'message' : 'Success'}, status = 201)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status = 404)

class MasterMatchingView(View):
    def get(self, request, service_id):
        user             = request.GET.get('user_id','')
        service          = Service.objects.get(id = service_id)
        application      = Application.objects.select_related('service').filter(service=service).get(user_id = user)
        matching_masters = ApplicationMaster.objects.select_related('master').filter(application=application)
        reviews          = Review.objects.select_related('master')
        results          = [{
                "image"        : matching_master.master.profile_image,
                "name"         : matching_master.master.name,
                "introduction" : matching_master.master.introduction,
                "rating"       : reviews.filter(master = matching_master.master).aggregate(Avg('rating'))["rating__avg"],
                "review"       : reviews.filter(master = matching_master.master).count()
            } for matching_master in matching_masters]

        return JsonResponse({'results' : results}, status = 200)
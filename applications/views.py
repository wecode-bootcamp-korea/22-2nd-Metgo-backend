import json
import datetime

from dateutil.relativedelta import relativedelta
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Avg

from masters.models         import Master,Region
from applications.models    import Application
from reviews.models         import Review
from core.views             import user_signin_check

class ApplicationView(View):
    @user_signin_check
    def post(self,request):
        try:
            data          = json.loads(request.body)
            age           = data['age']
            career        = data["career"]
            region        = Region.objects.get(name = data["region"])
            gender_choice = { "남" : "male", "여" : "female", "무관" : None }
            gender        = gender_choice[data["gender"]]
            
            Application.objects.update_or_create(
                service_id  = data["service_id"],
                user        = request.user,
                defaults    = { "age"     : age if age != '무관' else None,
                                "career"  : career,
                                "gender"  : gender,
                                "region"  : region}
            )
            
            return JsonResponse({ 'message' : 'Success' }, status = 201)
        
        except KeyError:
            return JsonResponse({ 'message' : 'KEY ERROR' }, status = 404)

class MastersView(View):
    @user_signin_check
    def get(self, request, service_id):
        user_id          = request.user
        application      = Application.objects.select_related('service').filter(service_id=service_id).get(user_id = user_id)
        gender           = application.gender
        age              = application.age
        career           = application.career
        region           = application.region

        q  = Q()
        q &= Q(main_service_id = service_id)
        
        q_career= Q(career__range = (career,career+5))
        q &= q_career if career !=15 else Q(career__gte = career)
        
        if gender:
            q &= Q(gender = gender)
        
        if region:
            q &= Q(region = region)

        if age:
            today = datetime.date.today()
            birth = today - relativedelta(year = today.year-age)
            q_age = Q(birth__range = (birth-relativedelta(year= birth.year-10), birth))
            q  &= q_age if age !=50 else Q(birth__lte = birth)
        
        masters = Master.objects.filter(q)

        results = [{
                "id"           : master.id,
                "image"        : master.profile_image,
                "name"         : master.name,
                "introduction" : master.introduction,
                "rating"       : master.review_set.all().aggregate(average = Avg('rating'))["average"],
                "review"       : master.review_set.all().count()
            } for master in masters]

        return JsonResponse({'results' : results}, status = 200)
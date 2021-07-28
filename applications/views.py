import json
import datetime
from dateutil.relativedelta import relativedelta
from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q, Avg
from users.models           import User
from masters.models         import Master,Region
from services.models        import Service
from applications.models    import Application 
from reviews.models         import Review
from core.views             import user_signin_check
class ApplicationView(View):
    @user_signin_check
    def post(self,request):
        try:
            data    = json.loads(request.body)
            age     = data["age"] if data["age"] != '무관' else None
            career  = data["career"]
            region  = Region.objects.get(name = data["region"])
            gender_choice = { "남" : "male", "여" : "female", "무관" : None }
            gender        = gender_choice[data["gender"]]
            Application.objects.update_or_create(
                service_id  = data["service_id"],
                user_id     = request.user,
                defaults    = { "age"     : age,
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
        if gender:
            q &= Q(gender = gender)
        if region:
            q &= Q(region = region)
        if age:
            today = datetime.date.today()
            birth = today - relativedelta(year = today.year-age)
            if age != 50:
                q  &= Q(birth__range = (birth-relativedelta(year= birth.year-10), birth))
            else:
                q  &= Q(birth__lte = birth)
        if career != 15:
            q &= Q(career__range = (career,career+5))
        else:
            q &= Q(career__gte = career)
        masters = Master.objects.filter(q)
        if not masters:
            return JsonResponse({'message' : 'Does not matching masters'}, status = 404)
        reviews          = Review.objects.select_related('master')
        results          = [{
                "image"        : master.profile_image,
                "name"         : master.name,
                "introduction" : master.introduction,
                "rating"       : reviews.filter(master = master).aggregate(average = Avg('rating'))["average"],
                "review"       : reviews.filter(master = master).count()
            } for master in masters]
        return JsonResponse({'results' : results}, status = 200)

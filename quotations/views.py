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
from quotations.models      import Quotation

class QuotationView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=data["user_id"])
        master = Master.objects.get(id=data["master_id"])
        application = Application.objects.filter(user=user).get(service=master.main_service)
        application_master = ApplicationMaster.objects.filter(application=application).get(master=master)
        Quotation.objects.create(
            application_master = application_master,
            master = master,
            price = None,
            is_comleted = 0,
        )

        return JsonResponse({'message' : 'Success'}, status = 201)

    def get(self, request):
        master_id = request.GET.get('master', '')
        quotations = Quotation.objects.select_related('application_master').filter(master_id=master_id)

        results = [{
            "quotation_id" : quotation.id,
            "user_id" : quotation.application_master.application.user.id,
            "user_name" : quotation.application_master.application.user.name,
        }for quotation in quotations]

        return JsonResponse({'results' : results}, status = 200)

    def patch(self, request):
        data = json.loads(request.body)
        quotation_id = data["quotation_id"]
        if data["is_complited"]:
            Quotation.objects.filter(id=quotation_id).update(is_complited = 1)
            return JsonResponse({'message' : 'Transaction Accepted'}, status = 201)
        
        Quotation.objects.get(id=quotation_id).delete()
        return JsonResponse({'message' : 'Transaction Denied'}, status = 201)
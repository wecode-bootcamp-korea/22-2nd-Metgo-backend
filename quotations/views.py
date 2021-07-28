import json
from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from masters.models         import Master
from applications.models    import Application
from quotations.models      import Quotation
from core.views import user_signin_check, master_signin_check

class QuotationView(View):
    @user_signin_check
    def post(self, request):
        data        = json.loads(request.body)
        user_id     = request.user
        master      = Master.objects.get(id=data["master_id"])
        application = Application.objects.filter(user_id=user_id).get(service=master.main_service)
        Quotation.objects.create(
            application = application,
            master      = master,
            price       = None,
        )
        return JsonResponse({'message' : 'Success'}, status = 201)

    @master_signin_check
    def get(self, request):
        master_id  = request.master
        quotations = Quotation.objects.select_related('application_master').filter(master_id=master_id)
        results    = [{
            "quotation_id" : quotation.id,
            "user_id" : quotation.application.user.id,
            "user_name" : quotation.application.user.name,
        } for quotation in quotations]
        return JsonResponse({'results' : results}, status = 200)

    @master_signin_check
    def patch(self, request):
        data         = json.loads(request.body)
        quotation_id = data["quotation_id"]
        if data["is_completed"]:
            Quotation.objects.filter(id=quotation_id).update(is_completed = 1)
            return JsonResponse({'message' : 'Transaction Accepted'}, status = 201)
        Quotation.objects.get(id=quotation_id).delete()
        return JsonResponse({'message' : 'Transaction Denied'}, status = 201)

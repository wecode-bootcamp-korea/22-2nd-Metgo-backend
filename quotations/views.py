import json

from django.http            import JsonResponse
from django.views           import View

from services.models        import MasterService
from quotations.models      import Quotation
from core.views             import user_signin_check, master_signin_check

class QuotationView(View):
    @user_signin_check
    def post(self, request):
        data            = json.loads(request.body)
        user            = request.user
        master_service  = MasterService.objects.get(id=data["master_id"])
        
        Quotation.objects.create(
            user            = user,
            master_services = master_service,
            status          = 'waiting'
        )

        return JsonResponse({ 'message' : 'Success' }, status = 201)

    @master_signin_check
    def get(self, request):
        master     = request.master
        quotations = Quotation.objects.filter(master=master)

        results = [{
            "quotation_id" : quotation.id,
            "user_id"      : quotation.user.id,
            "user_name"    : quotation.user.name,
        } for quotation in quotations ]

        return JsonResponse({ 'results' : results }, status = 200)

    @master_signin_check
    def patch(self, request):
        data         = json.loads(request.body)
        quotation_id = data["quotation_id"]
        status       = data["status"]

        Quotation.objects.filter(id=quotation_id).update(status = status)
        return JsonResponse({'message' : f'Transaction {status}'}, status = 201)

import json
from django.http            import JsonResponse
from django.views           import View
from users.models           import User
from masters.models         import Master
from applications.models    import Application
from quotations.models      import Quotation
class QuotationView(View):
    def post(self, request):
        data = json.loads(request.body)
        user = User.objects.get(id=data["user_id"])
        master = Master.objects.get(id=data["master_id"])
        application = Application.objects.filter(user=user).get(service=master.main_service)
        Quotation.objects.create(
            application = application,
            master = master,
            price = None,
        )
        return JsonResponse({'message' : 'Success', status = 201)
    def get(self, request):
        master_id = request.GET.get('master',)
        quotations = Quotation.objects.select_related('application_master').filter(master_id=master_id)
        results = [{
            "quotation_id" : quotation.id,
            "user_id" : quotation.application_master.application.user.id,
            "user_name" : quotation.application_master.application.user.name,
        } for quotation in quotations]
        return JsonResponse({'results' : results}, status = 200)
    def patch(self, request):
        data = json.loads(request.body)
        quotation_id = data["quotation_id"]
        if data["is_completed"]:
            Quotation.objects.filter(id=quotation_id).update(is_completed = 1)
            return JsonResponse({'message' : 'Transaction Accepted'}, status = 201)
        Quotation.objects.get(id=quotation_id).delete()
        return JsonResponse({'message' : 'Transaction Denied'}, status = 201)}

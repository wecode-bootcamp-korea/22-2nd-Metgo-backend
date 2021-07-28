from django.http                  import JsonResponse
from django.views                 import View
from django.core.paginator        import Paginator

from masters.models    import Master

class MasterReviewView(View):
    def get(self, request, master_id):
        try:
            if not Master.objects.filter(id=master_id).exists():
                return JsonResponse({'message':'DOES_NOT_EXISTS'}, status=400)

            master      = Master.objects.get(id=master_id)
            reviews     = master.review_set.filter(master_id=master.id)
            #  page        = request.GET.get('page', None)
            #  paginator   = Paginator(reviews, 5)
            #  review_list = paginator.get_page(page)
            #  total_pages = paginator.page_range

            results = [
                {
                    'name'       : review.user.name,
                    'rating'     : review.rating,
                    'created_at' : review.created_at,
                    'content'    : review.content
                } for review in reviews
            ]

            return JsonResponse({'results':results}, status=200)

        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

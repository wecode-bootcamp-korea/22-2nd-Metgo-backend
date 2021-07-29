from django.urls    import path

from quotations.views import QuotationView

urlpatterns = [
    path('', QuotationView.as_view())
]
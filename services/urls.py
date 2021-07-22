from django.urls    import path

from services.views import ServiceDetailView

urlpatterns = [
    path('/<str:service_id>', ServiceDetailView.as_view())
]
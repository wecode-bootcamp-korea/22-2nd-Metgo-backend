from django.urls    import path

from services.views import ServiceDetailView

urlpatterns = [
    path('/<int:service_id>', ServiceDetailView.as_view())
]
from django.urls    import path

from services.views import ServiceView

urlpatterns = [
    path('/<str:service_id>', ServiceView.as_view())
]
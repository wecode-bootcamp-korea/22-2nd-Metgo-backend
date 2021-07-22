from django.urls import path, include

from services.views import ServiceView

urlpatterns = [
    path('<int:category_id>', ServiceView.as_view()),
    path('services', include('services.urls')),
    path('applications', include('applications.urls')),
]

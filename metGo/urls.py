from django.urls import path, include

from services.views import ServiceView,CategoryView

urlpatterns = [
    path('', CategoryView.as_view()),
    path('<int:category_id>', ServiceView.as_view()),
    path('services', include('services.urls')),
    path('applications', include('applications.urls')),
    path('quotations', include('quotations.urls')),
]
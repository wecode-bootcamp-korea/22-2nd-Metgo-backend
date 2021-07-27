from django.urls import path, include

from services.views import ServiceView,CategoryView

urlpatterns = [
    path('categories', CategoryView.as_view()),
    path('categories/<int:category_id>', ServiceView.as_view()),
    path('services', include('services.urls')),
    path('applications', include('applications.urls')),
    path('quotations', include('quotations.urls')),
]
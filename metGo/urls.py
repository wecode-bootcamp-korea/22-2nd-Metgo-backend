from django.urls import path, include

from services.views import MainView

urlpatterns = [
    path('<str:category_name>', MainView.as_view()),
    path('applications', include('applications.urls'))
]

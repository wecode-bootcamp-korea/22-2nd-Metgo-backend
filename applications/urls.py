from django.urls import path, include

from applications.views import ApplicationView

urlpatterns = [
    path('', ApplicationView.as_view()),
]

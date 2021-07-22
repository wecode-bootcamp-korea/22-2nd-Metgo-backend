from django.urls import path, include

from applications.views import ApplicationView,MasterMatchingView

urlpatterns = [
    path('', ApplicationView.as_view()),
    path('/services/<int:service_id>/masters', MasterMatchingView.as_view()),
]

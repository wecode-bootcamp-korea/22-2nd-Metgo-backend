from django.urls import path
from applications.views import ApplicationView,MastersView
urlpatterns = [
    path('', ApplicationView.as_view()),
    path('/services/<int:service_id>/masters', MastersView.as_view()),
]

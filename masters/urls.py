from django.urls import path

from masters.views import MasterSignupView

urlpatterns = [
    path('/signup', MasterSignupView.as_view()),
]

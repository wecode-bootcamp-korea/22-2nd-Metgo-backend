from django.urls import path

from users.views import UserSignupView

urlpatterns = [
    path('/signup', UserSignupView.as_view()),
]

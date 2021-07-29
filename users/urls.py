from django.urls import path

from users.views import UserSignupView, UserSigninView, UserKakaoSigninView

urlpatterns = [
    path('/signup', UserSignupView.as_view()),
    path('/signin', UserSigninView.as_view()),
    path('/kakao/signin', UserKakaoSigninView.as_view()),
]

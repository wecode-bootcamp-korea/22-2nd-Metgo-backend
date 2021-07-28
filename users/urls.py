from django.urls import path

from users.views import UserSignupView, UserSigninView, KakaoSigninView

urlpatterns = [
    path('/signup', UserSignupView.as_view()),
    path('/signin', UserSigninView.as_view()),
    path('/kakao/signin', KakaoSigninView.as_view()),

]

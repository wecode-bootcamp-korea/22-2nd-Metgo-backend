from django.urls import path

from masters.views import MasterSignupView, MasterSigninView, MasterKakaoSigninView

urlpatterns = [
    path('/signup', MasterSignupView.as_view()),
    path('/signin', MasterSigninView.as_view()),
    path('/kakao/signin', MasterKakaoSigninView.as_view()),
]

from django.urls import path

from masters.views import MasterSignupView, MasterSigninView, MasterKakaoSigninView, MasterView

urlpatterns = [
    path('/signup', MasterSignupView.as_view()),
    path('/signin', MasterSigninView.as_view()),
    path('/kakao/signin', MasterKakaoSigninView.as_view()),
    path('/<int:master_id>', MasterView.as_view())
]

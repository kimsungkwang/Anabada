

from django.urls import path

from .views import KakaoLoginView, KakaoCallbackView

urlpatterns = [
    path('oauth/', KakaoLoginView.as_view()),
    path('oauth/callback', KakaoCallbackView.as_view()),
]
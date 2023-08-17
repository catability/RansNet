from django.urls import path
from users import views

urlpatterns = [
    path("login/", views.user_login),
    path("sign/", views.user_sign),
    path("sign/check-username/", views.check_username),
    path("profile/", views.mypage),
]

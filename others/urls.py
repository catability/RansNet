from django.urls import path
from others import views

urlpatterns = [
    path("info/", views.info),
    path("guide/", views.guide),
]

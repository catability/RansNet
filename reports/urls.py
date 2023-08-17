from django.urls import path
from reports import views

urlpatterns = [
    path("report/", views.report_register),
    path("reports/", views.report_list),
    path("reports/search-word/", views.report_search),
    path("reports/<int:pk>", views.report_detail),
]

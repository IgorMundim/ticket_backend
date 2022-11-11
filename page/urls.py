from django.urls import path

from page import views

app_name = "pages"

urlpatterns = [
    path("home/", views.home, name="home"),
    path("base/", views.base, name="base"),
]

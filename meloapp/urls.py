from django.contrib import admin
from django.urls import path
from melo import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),
    path("vote/", views.vote, name="vote"),
]

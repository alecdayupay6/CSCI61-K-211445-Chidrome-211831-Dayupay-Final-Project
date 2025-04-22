from django.urls import path
from . import views

urlpatterns = [
    path("", views.register, name="register"),
    path("register/", views.register, name="register"),
    path("login/", views.login_, name="login"),
    path("search/", views.search, name="search"),
    path("delete/", views.delete_, name="delete"),
    path("logout/", views.logout_, name="logout"),
]
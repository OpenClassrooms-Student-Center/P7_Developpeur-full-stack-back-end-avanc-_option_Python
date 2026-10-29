from django.urls import path

from . import views

urlpatterns = [
    path("connexion/", views.login_view, name="login"),
]

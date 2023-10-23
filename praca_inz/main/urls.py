from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recognition/", views.model, name="model_page"),
]

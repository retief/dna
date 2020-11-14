from django.urls import path

from api import views

urlpatterns = [
    path("startSearch", views.start_search, name="start_search"),
]

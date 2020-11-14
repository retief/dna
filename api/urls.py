from django.urls import path

from api import views

urlpatterns = [
    path("search", views.start_search, name="start_search"),
    path("results", views.search_results, name="search_results"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.wiki_page, name="page"),
    path("search/<str:query>", views.search, name="search")
]

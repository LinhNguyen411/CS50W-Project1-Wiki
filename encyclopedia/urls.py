from django.urls import path

from . import views
from . import util

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:entry>", views.template, name="entry"),
    path("wiki/<str:entry>/edit", views.edit, name="edit"),
    path("search_result", views.search_result, name="search"),
    path("create", views.create, name="create"),
    path("random", views.ran_entry, name="random")
]



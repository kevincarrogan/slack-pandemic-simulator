from django.urls import path

from . import views

app_name = "people"

urlpatterns = [
    path("", views.PersonView.as_view(), name="person"),
]

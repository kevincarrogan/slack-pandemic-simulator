from django.urls import include, path

from . import views

app_name = "messages"

urlpatterns = [
    path("", views.MessageView.as_view(), name="message"),
]

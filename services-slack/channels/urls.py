from django.urls import include, path

from . import views

app_name = "channels"

urlpatterns = [
    path("member/", views.MemberView.as_view(), name="member"),
]

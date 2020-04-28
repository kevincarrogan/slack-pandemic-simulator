from django.urls import include, path

urlpatterns = [
    path("channel/", include("channels.urls")),
    path("message/", include("messages.urls")),
]

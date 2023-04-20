from django.urls import path

from . import views

urlpatterns = [
    path(
        "user-reply/",
        views.user_reply,
        name="user-reply"
    ),
]

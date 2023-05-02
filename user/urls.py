from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path("user/", include("user.api.urls", namespace="user_api")),
]
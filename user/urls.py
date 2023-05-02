from django.urls import path, include

app_name = 'user'

urlpatterns = [
    path("api/", include("user.user_api.urls", namespace="user_api")),
]
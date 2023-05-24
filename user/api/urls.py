from django.urls import path
from .views import (DummyView, RegisterView, UserDetailsAPIView, UserImageUploadAPIView, UpdateUserAPIView,
FetchUserInfo, CreateEvent, FetchEvents)


app_name = "user_api"


urlpatterns = [
    path("dummy/", DummyView.as_view(), name="dummy"),
    path("register/", RegisterView.as_view(), name='register'),
    path("user/", UserDetailsAPIView.as_view(), name='user'),
    path("update_image/", UserImageUploadAPIView.as_view(), name="image"),
    path("update_user/", UpdateUserAPIView.as_view(), name="user_update"),
    path("fetch_user_info/", FetchUserInfo.as_view(), name="user_info"),
    path("create_event/", CreateEvent.as_view(), name="create_event"),
    path("fetch_event/", FetchEvents.as_view(), name="fetch_event"),
]
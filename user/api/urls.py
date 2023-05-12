from django.urls import path
from .views import DummyView, RegisterView, UserDetailsAPIView, UserImageUploadAPIView


app_name = "user_api"


urlpatterns = [
    path("dummy/", DummyView.as_view(), name="dummy"),
    path("register/", RegisterView.as_view(), name='register'),
    path("user/", UserDetailsAPIView.as_view(), name='user'),
    path("update_image/", UserImageUploadAPIView.as_view(), name="image"),
]
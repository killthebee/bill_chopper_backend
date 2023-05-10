from django.urls import path
from .views import DummyView, RegisterView, UserDetailsAPIView


app_name = "user_api"


urlpatterns = [
    path("dummy/", DummyView.as_view(), name="dummy"),
    path("register/", RegisterView.as_view(), name='register'),
    path("user/", UserDetailsAPIView.as_view(), name='user')
]
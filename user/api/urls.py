from django.urls import path
from .views import DummyView, RegisterView


app_name = "user_api"


urlpatterns = [
    path("dummy/", DummyView.as_view(), name="dummy"),
    path("register/", RegisterView.as_view(), name='register')
]
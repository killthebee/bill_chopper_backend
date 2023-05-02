from django.urls import path
from .views import DummyView


app_name = "user_api"


urlpatterns = [
    # path("clients/create", SignUpUser.as_view(), name="sing_up"),
    path("dummy/", DummyView.as_view(), name="dummy"),
]
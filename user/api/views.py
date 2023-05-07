from rest_framework import generics
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import RegisterUserSerializer


class DummyView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({"task_id": "111", "Success": True, "hi_to": "Post"})

    def get(self, request, *args, **kwargs):
        return Response({"task_id": "111", "Success": True, "hi_to": "GET"})


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer

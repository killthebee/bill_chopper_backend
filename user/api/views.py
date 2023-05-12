from rest_framework import generics, status
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from .serializers import RegisterUserSerializer, UserSerializer, UpdateUserImageSerializer


class DummyView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request, *args, **kwargs):
        print(request.data)
        return Response({"task_id": "111", "Success": True, "hi_to": "Post"})

    def get(self, request, *args, **kwargs):
        return Response({"task_id": "111", "Success": True, "hi_to": "GET"})


class RegisterView(generics.CreateAPIView):
    """
    Register user!
    """
    queryset = User.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = RegisterUserSerializer


class UserDetailsAPIView(generics.RetrieveAPIView):
    """
    Retrieve user details!
    """
    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        username = self.request.user.username
        filter_kwargs = {self.lookup_field: username}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj


class UserImageUploadAPIView(APIView):
    """
    API view for CustomUser to upload user's photo.

    Request Type: POST.
    """
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, FormParser,)

    def post(self, request, format=None):
        print(request.data)
        serializer = UpdateUserImageSerializer(
            data=request.data, instance=request.user.profile)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
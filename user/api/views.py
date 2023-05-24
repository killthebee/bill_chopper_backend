from rest_framework import generics, status
from django.contrib.auth.models import User
from user.models import Event, Spend
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser
from .serializers import (RegisterUserSerializer, RetriveUserSerializer, UpdateUserImageSerializer,
                          UpdateUserSerializer, CreateEventSerializer, ParticipantsSerializer,
                          EventSerializer)


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
    serializer_class = RetriveUserSerializer

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


class UpdateUserAPIView(generics.UpdateAPIView):
    """
    Api to update User and profile
    """

    permission_classes = (IsAuthenticated, )
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = UpdateUserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        username = self.request.user.username
        filter_kwargs = {self.lookup_field: username}
        obj = get_object_or_404(queryset, **filter_kwargs)

        self.check_object_permissions(self.request, obj)

        return obj

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        profile = instance.profile
        data = request.data
        print(data)
        if 'is_male' in data:
            profile.is_male = data['is_male']
        if 'first_name' in data:
            instance.first_name = data['first_name']
        if 'username' in data:
            instance.username = data['username']
        instance.save()
        profile.save()
        return Response(data={"success": True}, status=status.HTTP_200_OK)


class FetchUserInfo(generics.RetrieveAPIView):
    """
    Retrive user info if the user exists
    """
    permission_classes = (IsAuthenticated, )
    # allowed_methods = ("GET", "POST", )
    queryset = User.objects.all()
    lookup_field = 'username'
    serializer_class = RetriveUserSerializer

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        print(self.request.data)
        username = self.request.data["username"]
        filter_kwargs = {self.lookup_field: username}
        obj = get_object_or_404(queryset, **filter_kwargs)
        print(obj)
        self.check_object_permissions(self.request, obj)

        return obj

    def post(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


class CreateEvent(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Event.objects.all()
    serializer_class = CreateEventSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users = request.data['participants']
        for user in users:
            users_serializer = ParticipantsSerializer(data=user)
            if users_serializer.is_valid():
                users_serializer.save()
            else:
                return

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateSpend(generics.CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Spend.objects.all()


class FetchEvents(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Event.objects.all()
    lookup_field = 'participants'
    serializer_class = EventSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(participants=self.request.user)
        return queryset

    # def get_object(self):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     print(self.request.data)
    #     username = self.request.user
    #     filter_kwargs = {self.lookup_field: username}
    #     obj = get_object_or_404(queryset, **filter_kwargs)
    #     print(obj)
    #     self.check_object_permissions(self.request, obj)
    #
    #     return obj


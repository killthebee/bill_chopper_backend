import json
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
                          EventSerializer, CreateSpendSerializer, RetrieveEventsSpendsSerializer)


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
        print(users)
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
    serializer_class = CreateSpendSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        payeer = User.objects.get(username=request.data['payeer']['username'])
        event = Event.objects.get(pk=request.data['event']['id'])
        spend = Spend.objects.create(
            payeer=payeer,
            event=event,
            name=request.data['name'],
            split=request.data['split'],
            date=request.data['date'],
            amount=request.data['amount'],
        )
        spend.save()
        return Response({"success": True, "spendId": spend.id}, status=status.HTTP_201_CREATED)


class FetchEvents(generics.ListAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = Event.objects.all()
    lookup_field = 'participants'
    serializer_class = EventSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(participants=self.request.user)
        return queryset


class FetchEventsSpends(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Event.objects.all()
    serializer_class = RetrieveEventsSpendsSerializer

    def filter_queryset(self, queryset):
        queryset = queryset.filter(participants=self.request.user)
        print(self.request.authenticators)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        for event in serializer.data:
            spends = event['spends']
            for spend in spends:
                hm = json.loads(spend['split'])
                spend['split'] = hm
        return Response(serializer.data)


class DeleteSpendSerializer(generics.DestroyAPIView):
    model = Spend
    permission_classes = (IsAuthenticated, )
    queryset = Spend.objects.all()
    serializer_class = CreateSpendSerializer
    # lookup_field = "pk"

    def get_authenticators(self):
        """
        Instantiates and returns the list of authenticators that this view can use.
        """

        return [auth() for auth in self.authentication_classes]

    # def _allowed_methods(self):
    #     print(self.request.authenticators)
    #     return [m.upper() for m in self.http_method_names if hasattr(self, m)]
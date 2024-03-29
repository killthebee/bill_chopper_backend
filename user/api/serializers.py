from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from user.models import Profile, EventParticipants, Event, Spend


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('is_male', 'profile_image', )


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', )


class SimpleUserSerializer(serializers.Serializer):

    class Meta:
        fields = ('username', )


class RegisterUserSerializer(UserSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('password', 'first_name', )

    def create(self, validated_data):
        user = User.objects.create(
            email=f"{validated_data['username']}@mail.ru",
            username=validated_data['username'],
        )
        user.first_name = validated_data['first_name']
        user.set_password(validated_data['password'])
        user.save()

        return user


class EventSerializer(serializers.ModelSerializer):
    participants = UserSerializer(many=True, required=False)

    class Meta:
        model = Event
        fields = ('id', 'event_type', 'name', 'participants', )


class RetriveUserSerializer(UserSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = User
        fields = UserSerializer.Meta.fields + ('first_name', 'profile', )


class UpdateUserImageSerializer(serializers.ModelSerializer):
    """
    Changes the user's profile image.

    Fields: profile_image.
    """
    profile_image = serializers.ImageField(required=True)

    class Meta:
        model = Profile
        fields = ('profile_image', )

    def save(self, *args, **kwargs):
        if self.instance.profile_image:
            self.instance.profile_image.delete()

        return super().save(*args, **kwargs)


class UpdateUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'profile', )


class ParticipantsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, write_only=True, required=True)
    def create(self, validated_data):
        user = User.objects.get_or_create(username=validated_data['username'])
        return user

    class Meta:
        model = User
        fields = ('username', )


class CreateEventSerializer(serializers.ModelSerializer):
    participants = ParticipantsSerializer(many=True, required=True)

    def validate_participants(self, value):
        if len(value) == 0:
            raise serializers.ValidationError({"participants": "No participants provided"})

        return value

    def create(self, validated_data):
        users = validated_data.pop('participants')
        event = Event.objects.create(**validated_data)
        for user in users:
            event_participant, is_created = User.objects.get_or_create(username=user['username'])
            EventParticipants.objects.create(user=event_participant, event=event)
        return event

    class Meta:
        model = Event
        fields = ('name', 'event_type', 'participants', "id")


class CreateSpendSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)
    payeer = SimpleUserSerializer(read_only=True)

    class Meta:
        model = Spend
        fields = ('name', 'event', 'payeer', 'split', 'date')


class RetrieveSpendSerializer(serializers.ModelSerializer):
    payeer = RetriveUserSerializer()

    class Meta:
        model = Spend
        fields = ('name', 'event', 'payeer', 'split', 'date', 'amount', 'id')


class RetrieveEventsSpendsSerializer(serializers.ModelSerializer):
    participants = RetriveUserSerializer(many=True)
    spends = RetrieveSpendSerializer(many=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'event_type', 'participants', 'spends', )

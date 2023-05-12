from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from user.models import Profile


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', )

    def create(self, validated_data):
        user = User.objects.create(
            email=f"{validated_data['username']}@mail.ru",
            username=validated_data['username'],
        )
        user.first_name = validated_data['first_name']
        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('first_name', 'username', )


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
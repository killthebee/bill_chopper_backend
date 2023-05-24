import os
from django.db import models
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


def upload_to(instance, filename):
    """
    Changed the output of the photo name.
    """
    now = timezone.now()
    base, extension = os.path.splitext(filename.lower())
    milliseconds = now.microsecond // 1000
    return f"images/user/{instance.id}/{now:%Y%m%d%H%M%S}{milliseconds}{extension}"


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=upload_to)
    is_male = models.BooleanField(default=True)


class Event(models.Model):
    TRIP, PURCHASE, PARTY, OTHER = 1, 2, 3, 4
    TYPES = (
        (TRIP, "trip"),
        (PURCHASE, "purchase"),
        (PARTY, "party"),
        (OTHER, "other"),
    )
    event_type = models.PositiveIntegerField(
        default=OTHER,
        choices=TYPES,
        db_index=True
    )
    name = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, through="EventParticipants", )


class EventParticipants(models.Model):
    user = models.ForeignKey(User, related_name="users", on_delete=models.CASCADE)
    event = models.ForeignKey(Event, related_name="events", on_delete=models.CASCADE)


class Spend(models.Model):
    name = models.CharField(max_length=50)
    event = models.ForeignKey(Event, related_name="spends", on_delete=models.CASCADE)
    payeer = models.ForeignKey(User, on_delete=models.CASCADE)
    split = models.JSONField(null=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
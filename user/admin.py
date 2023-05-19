from django.contrib import admin
from .models import Profile, Event, EventParticipants

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventParticipants)

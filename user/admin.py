from django.contrib import admin
from .models import Profile, Event, EventParticipants, Spend

admin.site.register(Profile)
admin.site.register(Event)
admin.site.register(EventParticipants)
admin.site.register(Spend)

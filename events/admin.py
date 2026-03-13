from django.contrib import admin
from events.models import Event, EventDetail, Project

# Register your models here.
admin.site.register(Event)
admin.site.register(EventDetail)
admin.site.register(Project)
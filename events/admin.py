from django.contrib import admin
from .models import Category, Event, Participant

# Register your models here.
admin.site.register(Category)
admin.site.register(Event)
admin.site.register(Participant)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'location')
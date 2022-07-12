from django.contrib import admin
from .models import Event
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):

    list_display = ('title', 'category', 'created_on', 'location_time')
    search_fields = ['title', 'summary']
    list_filter = ('created_on', 'location_time')
    summernote_fields = ('summary')

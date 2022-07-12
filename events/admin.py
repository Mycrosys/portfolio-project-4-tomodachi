from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Event


@admin.register(Event)
class EventAdmin(SummernoteModelAdmin):
    """
    Basic configuration for an easier to use Admin Panel with Summernote
    """

    # Displays, Search and Filter for Admin Panel
    list_display = ('title', 'category', 'created_on', 'location_time')
    search_fields = ['title', 'summary']
    list_filter = ('created_on', 'location_time')

    # WYSIWYG edit field for summary of the Event
    summernote_fields = ('summary')

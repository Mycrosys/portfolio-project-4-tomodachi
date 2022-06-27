from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Event
from django.utils.timezone import datetime
from django.utils import timezone


class EventList(generic.ListView):
    model = Event
    template_name = 'index.html'

    def get_queryset(self):
        return Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())



class EventDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)
        attendee = False
        if event.attendees.filter(id=self.request.user.id).exists():
            attendee = True

        return render(
            request,
            "event_detail.html",
            {
                "event": event,
                "attendee": attendee
            },
        )


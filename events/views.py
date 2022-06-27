from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Event
from django.utils.timezone import datetime


class EventList(generic.ListView):
    model = Event
    queryset = Event.objects.order_by('location_time').filter(location_time__time__gte=datetime.now())
    template_name = 'index.html'
    paginate_by = 25

class EventDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Event.objects.filter(location_time__time__gte=datetime.now())
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


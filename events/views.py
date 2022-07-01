from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.utils import timezone
from .models import Event
from .forms import EventForm


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
            },
        )


class EventCreate(View):

    def get(self, request):
        return render(
            request,
            "create_event.html",
            {
                "event_form": EventForm()
            },
        )

    def post(self, request):
        
        event_form = EventForm(data=request.POST)
        
        if event_form.is_valid():
            event_form.instance.author = request.user
            event_form.instance.slug = event_form.instance.title.replace(" ", "-")
            event = event_form.save()
            event.attendees.add(request.user)

        else:
            event_form = EventForm()
            
        return redirect('home')

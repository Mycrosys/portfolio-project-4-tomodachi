from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.utils import timezone
from django.contrib import messages
from .models import Event
from .forms import EventForm


class EventList(generic.ListView):
    model = Event
    template_name = 'index.html'

    def get_queryset(self):
        return Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())


class EventDetail(View):

    def get(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)

        return render(
            request,
            "event_detail.html",
            {
                "event": event,
            },
        )


class EventMy(generic.ListView):

    def get(self, request):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        created_event = queryset.filter(author=self.request.user.id)
        joined_event = queryset.filter(attendees=self.request.user.id)

        return render(
            request,
            "my_events.html",
            {
                "created_events": created_event,
                "joined_events": joined_event,
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
            event = event_form.save()
            event.slug = "eventid_" + str(event.id)
            event.save()
            event.attendees.add(request.user)
            feedback = "Successfully created Event " + event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            feedback = "Submission invalid. Please try again."
            messages.add_message(request, messages.ERROR, feedback)
            event_form = EventForm()

        return redirect('my_events')


class EventDelete(View):

    def get(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)
        if (request.user == event.author):
            feedback = "Successfully deleted Event " + event.title + "."
            event.delete()
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            feedback = "You are not the owner of Event " + event.title + " and can't delete it."
            messages.add_message(request, messages.ERROR, feedback)

        return redirect('my_events')


class EventRemoveAttendee(View):

    def get(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)
        event.attendees.remove(request.user)
        feedback = "You were successfully removed as Attendee from Event " + event.title + "."
        messages.add_message(request, messages.SUCCESS, feedback)
        return redirect('my_events')


class EventAddAttendee(View):

    def get(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)
        event.attendees.add(request.user)
        feedback = "You were successfully added as Attendee for Event " + event.title + "."
        messages.add_message(request, messages.SUCCESS, feedback)
        return redirect('my_events')


class EventEdit(View):

    def get(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)
        
        event_form = EventForm(instance=event)
        
        return render(
            request,
            "edit_event.html",
            {
                "event_form": event_form
            },
        )
    
    def post(self, request, slug):
        queryset = Event.objects.order_by('location_time').filter(location_time__gt=timezone.now())
        event = get_object_or_404(queryset, slug=slug)

        event_form = EventForm(data=request.POST, instance=event)

        if event_form.is_valid():
            event_form.instance.slug = event_form.instance.title.replace(" ", "-")
            event = event_form.save()
            feedback = "Successfully modified Event " + event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            event_form = EventForm()

        return redirect('my_events')
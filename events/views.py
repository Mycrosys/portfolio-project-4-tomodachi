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
        # Filter Events to only the ones that happen now and in the future
        return Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())


class EventDetail(View):

    def get(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())
        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        return render(
            request,
            "event_detail.html",
            {
                "event": event,
            },
        )


class EventMy(View):

    def get(self, request):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())
        # Created Events are the ones the logged in user is the author
        created_event = queryset.filter(author=self.request.user.id)
        # Joined Events are the ones the logged in user is an attendee
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

        # Get the Values from the Event Form
        event_form = EventForm(data=request.POST)

        # Check if form is valid
        if event_form.is_valid():
            # Set the author to the logged in user
            event_form.instance.author = request.user
            # Save the form to create an Event ID automatically
            # The Event ID is only created with saving,
            # so this is a necessary step
            event = event_form.save()
            # Create the slug out of the Event ID and a string
            event.slug = "eventid_" + str(event.id)
            # Save it again
            event.save()
            # Add the current User as Attendee (required)
            event.attendees.add(request.user)
            # Create a feedback message that the Event was created
            feedback = "Successfully created Event " + event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            # If the form is not valid, create and display an Error message
            feedback = "Submission invalid. Please try again."
            messages.add_message(request, messages.ERROR, feedback)
            
        # redirect to My Events
        return redirect('my_events')


class EventDelete(View):

    def get(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())
        
        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)
        
        # Event Deletion only allowed for event creator so check that
        if request.user == event.author:
            # Create a feedback message that the Event was deleted
            # and delete the Event
            feedback = "Successfully deleted Event " + event.title + "."
            event.delete()
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            # Create a feedback message that the Event was not deleted
            feedback = "You are not the owner of Event " + event.title
            feedback += " and can't delete it."
            messages.add_message(request, messages.ERROR, feedback)

        # redirect to My Events
        return redirect('my_events')


class EventRemoveAttendee(View):

    def get(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())

        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        # Remove the current logged in User from the list of attendees
        event.attendees.remove(request.user)

        # Create a feedback message that User was removed from attendees
        feedback = "You were successfully removed as Attendee from Event "
        feedback += event.title + "."
        messages.add_message(request, messages.SUCCESS, feedback)

        # redirect to My Events
        return redirect('my_events')


class EventAddAttendee(View):

    def get(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())

        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        # Add the current logged in User to the list of attendees
        event.attendees.add(request.user)

        # Create a feedback message that User was added to attendees
        feedback = "You were successfully added as Attendee for Event "
        feedback += event.title + "."
        messages.add_message(request, messages.SUCCESS, feedback)

        # redirect to My Events
        return redirect('my_events')


class EventEdit(View):

    def get(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())
        
        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        # Get and fill the Event Form with the Data from the Event
        event_form = EventForm(instance=event)

        return render(
            request,
            "edit_event.html",
            {
                "event_form": event_form
            },
        )

    def post(self, request, pk):
        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())
        
        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        # Get the Values from the Event Form
        event_form = EventForm(data=request.POST, instance=event)

        # Check if form is valid
        if event_form.is_valid():
            # Save the form to create an Event ID automatically
            event = event_form.save()
            # This step isn't actually needed, but it is done to fix
            # Slugs created by Events in the Admin Panel
            # All Events created via the Form on the Website already
            # have the correct slug
            event.slug = "eventid_" + str(event.id)
            event.save()
            # Create a feedback message that the Event was updated
            feedback = "Successfully modified Event " + event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            # If the form is not valid, create and display an Error message
            feedback = "Submission invalid. Please try again."
            messages.add_message(request, messages.ERROR, feedback)

        # redirect to My Events
        return redirect('my_events')

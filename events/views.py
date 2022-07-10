from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.utils import timezone
from django.contrib import messages
from .models import Event
from .forms import EventForm


class EventList(generic.ListView):
    """
    Displays the Index Page with the upcoming Events. The Template only
    takes a slice of 4, but all Events in the future are returned.
    """

    model = Event
    template_name = 'index.html'

    def get_queryset(self):
        # Filter Events to only the ones that happen now and in the future
        return Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())


class EventDetail(View):
    """
    Displays the Event Detail Page of a certain selected
    Event (defined by Event ID)
    """

    def get(self, request, pk):
        """
        Displays the Event Detail Page with the Event ID
        """

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
    """
    Displays the My Events Page with created and joined Events by
    the logged in User.
    """

    def get(self, request):
        """
        Displays the My Events Page and returns created Events by User
        as well as joined Events.
        """

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
    """
    Displays the Form to create a new Event (get) and handles the creation
    in post. Also triggers a message to inform the User once it finishes.
    """

    def get(self, request):
        """
        Displays the Create Events Page with the form.
        """

        return render(
            request,
            "create_event.html",
            {
                "event_form": EventForm()
            },
        )

    def post(self, request):
        """
        Handles the Form and creates new Database Entry
        """

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
    """
    Handles the deletion of an Event and redirects to the My Event Page
    afterwards. Also Triggers a message upon completion.
    """

    def get(self, request, pk):
        """
        Deletes the Event after checking if the logged in User is the
        creator of the Event.
        """

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
    """
    Handles the removal of the logged in User from an Event and redirects
    to the My Event Page afterwards. Also triggers a message upon completion.
    """

    def get(self, request, pk):
        """
        Removes the participation of the logged in User in an Event
        """

        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())

        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        # Check if logged in User is in attendees
        if request.user in event.attendees.all():
            # Remove the current logged in User from the list of attendees
            event.attendees.remove(request.user)

            # Create a feedback message that User was removed from attendees
            feedback = "You were successfully removed as Attendee from Event "
            feedback += event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        else:
            # Create a feedback message that User isn't in attendees
            feedback = "You haven't joined Event "
            feedback += event.title + " yet and therefore cannot be removed"
            messages.add_message(request, messages.ERROR, feedback)

        # redirect to My Events
        return redirect('my_events')


class EventAddAttendee(View):
    """
    Handles the adding of the logged in User as Event attendee and redirects
    to the My Event Page afterwards. Also triggers a message upon completion.
    """

    def get(self, request, pk):
        """
        Adds the participation of the logged in User in an Event
        """

        # Filter Events to only the ones that happen now and in the future
        queryset = Event.objects.order_by('location_time').filter(
            location_time__gt=timezone.now())

        # Use the Event ID to get the correct Event
        event = get_object_or_404(queryset, pk=pk)

        if request.user in event.attendees.all():
            # Create a feedback message that User is already an attendee
            feedback = "You are already an Attendee for Event "
            feedback += event.title + "."
            messages.add_message(request, messages.ERROR, feedback)    
        
        else:
            # Add the current logged in User to the list of attendees
            event.attendees.add(request.user)

            # Create a feedback message that User was added to attendees
            feedback = "You were successfully added as Attendee for Event "
            feedback += event.title + "."
            messages.add_message(request, messages.SUCCESS, feedback)

        # redirect to My Events
        return redirect('my_events')


class EventEdit(View):
    """
    Displays the Form with an existing Event prefilled (get) and handles
    the update/editing in post. Also triggers a message to inform the User
    once it finishes.
    """

    def get(self, request, pk):
        """
        Displays the Modify Event Page with the form prefilled with Data
        from the Event with the used Event ID
        """

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
        """
        Handles the Form and updated the Database Entry
        """

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

from django.db import models
from django.contrib.auth.models import User


class Event(models.Model):
    """
    Event Model that contains all Information for an Event

    -----------------------------------------------------------------
    title:           The Title of the Event
    -----------------------------------------------------------------
    author:          The creator of the Event
    -----------------------------------------------------------------
    created_on:      Time the Event was first created in the Database
    -----------------------------------------------------------------
    modified_on:     Time of last modification of the Database Entry.
    -----------------------------------------------------------------
    summary:         The Bulk of the Information of said Event. What
                     is planned, how is it supposed to unfold, etc.
    -----------------------------------------------------------------
    attendees:       Contains all the Users attending the Event.
    -----------------------------------------------------------------
    category:        The Event Category.
    -----------------------------------------------------------------
    location_online: If the Event doesn't need physical attendance
                     but instead uses Online resources (e.g Discord)
    -----------------------------------------------------------------
    location_area:   The Location it takes place (e.g. address)
    -----------------------------------------------------------------
    location_time:   The Time the Event starts.
    -----------------------------------------------------------------
    """

    # Cathegories are listed here
    DINING = 'DIN'
    CINEMA = 'CIN'
    GAMING = 'GAM'
    SPORTS = 'SPO'
    CAMPING = 'CAM'
    CATEGORY_CHOICES = [
        (DINING, 'Dining'),
        (CINEMA, 'Cinema'),
        (GAMING, 'Gaming'),
        (SPORTS, 'Sports'),
        (CAMPING, 'Camping'),
    ]

    title = models.CharField(max_length=200, unique=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name="event_post")
    modified_on = models.DateTimeField(auto_now=True)
    summary = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(User, related_name='event_attendees',
                                       blank=True)
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=DINING,
    )
    location_online = models.BooleanField(default=False)
    location_area = models. TextField()
    location_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        """
        Metaclass - Ordering by Time the Events takes place
        """

        ordering = ['-location_time']

    def __str__(self):
        """
        Returns the name of an Event
        """

        return self.title

    def number_of_attendees(self):
        """
        Returns the number of attendees of an Event
        """

        return self.attendees.count()

    def category_verbose(self):
        """
        Prints out the name of the choosen category of an Event
        """

        return dict(Event.CATEGORY_CHOICES)[self.category].lower()

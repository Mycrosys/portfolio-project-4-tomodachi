from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Event(models.Model):
    DINNING = 'DIN'
    CINEMA = 'CIN'
    GAMING = 'GAM'
    SPORTS = 'SPO'
    CAMPING = 'CAM'
    CATEGORY_CHOICES = [
        (DINNING, 'Dinning'),
        (CINEMA, 'Cinema'),
        (GAMING, 'Gaming'),
        (SPORTS, 'Sports'),
        (CAMPING, 'Camping'),
    ]

    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="event_post")
    modified_on = models.DateTimeField(auto_now=True)
    summary = models.TextField()
    excerpt = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    attendees = models.ManyToManyField(User, related_name='event_attendees', blank=True)
    category = models.CharField(
        max_length=3,
        choices=CATEGORY_CHOICES,
        default=DINNING,
    )
    location_online = models.BooleanField(default=False)
    location_area = models. TextField()
    location_time = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-location_time']

    def __str__(self):
        return self.title

    def number_of_attendees(self):
        return self.attendees.count()

    def category_verbose(self):
        return dict(Event.CATEGORY_CHOICES)[self.category].lower()


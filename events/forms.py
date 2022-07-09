from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event

        fields = ('title', 'category', 'summary', 'location_area',
                  'location_online', 'location_time')
        widgets = {
            'location_area': forms.Textarea(attrs={'rows': 3}),
            'location_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'})
        }

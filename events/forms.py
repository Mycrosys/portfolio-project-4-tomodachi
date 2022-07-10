from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    """
    Form to Create new Events and Update existing ones
    """

    class Meta:
        """
        Metaclass to configure the form
        """
        model = Event

        fields = ('title', 'category', 'summary', 'location_area',
                  'location_online', 'location_time')

        # Overriding the widgets, Location Area doesn't need more than
        # 3 rows and using a Date and Time Picker for the location time
        widgets = {
            'location_area': forms.Textarea(attrs={'rows': 3}),
            'location_time': forms.DateTimeInput(
                attrs={'type': 'datetime-local'})
        }

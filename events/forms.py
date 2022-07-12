from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Column, Row, Fieldset, Submit, Reset
from crispy_forms.layout import Div
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


class BrowseForm(forms.Form):
    """
    Form to Browse/Filter Events
    """

    online = forms.BooleanField(required=False,
                                initial=True, label='Online Events')
    offline = forms.BooleanField(required=False,
                                 initial=True, label='Offline Events')
    searchstring = forms.CharField(required=False,
                                   max_length=50,
                                   label='Search Title, Summary and Location')
    dining = forms.BooleanField(required=False, initial=True)
    cinema = forms.BooleanField(required=False, initial=True)
    gaming = forms.BooleanField(required=False, initial=True)
    sports = forms.BooleanField(required=False, initial=True)
    camping = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        # self.helper.add_input(Submit('submit', 'Filter',
        #                      css_class='btn btn-crispy'))

        # self.helper.add_input(Reset('reset', 'Reset',
        #                      css_class='btn btn-crispy'))

        self.helper.form_method = 'POST'
        self.helper.layout = Layout(
            'searchstring',

            Row(
                Column('online', css_class='col-md-6 mb-0'),
                Column('offline', css_class='col-md-6 mb-0'),
                css_class='text-center'),

            Fieldset(
                'Categories',
                Row(
                    Column('dining', css_class='col-md-4 mb-0'),
                    Column('cinema', css_class='col-md-4 mb-0'),
                    Column('gaming', css_class='col-md-4 mb-0'),
                    css_class='category-form'),
                Row(
                    Column('sports', css_class='col-md-4 mb-0'),
                    Column('camping', css_class='col-md-4 mb-0'),
                    css_class='category-form',),
            ),

            Div(Submit('submit', 'Filter', css_class='btn btn-crispy'),
                Reset('reset', 'Reset', css_class='btn btn-crispy'),
                css_class='text-center',)
        )

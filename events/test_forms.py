from django.test import TestCase
from .forms import EventForm, BrowseForm


class TestEventForm(TestCase):
    """
    Tests for EventForm, which is used both for creating an Event and
    for modifying existing Events.
    """

    def test_event_title_is_required(self):
        """
        Tests if the title Field in the Event Form requires an entry
        Pass: Entry required
        """
        form = EventForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_event_category_is_required(self):
        """
        Tests if the category Field in the Event Form requires an entry
        Pass: Entry required
        """
        form = EventForm({'category': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors.keys())
        self.assertEqual(form.errors['category'][0], 'This field is required.')

    def test_event_summary_is_required(self):
        """
        Tests if the summary Field in the Event Form requires an entry
        Pass: Entry required
        """
        form = EventForm({'summary': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('summary', form.errors.keys())
        self.assertEqual(form.errors['summary'][0], 'This field is required.')

    def test_event_location_area_is_required(self):
        """
        Tests if the location_area Field in the Event Form requires an entry
        Pass: Entry required
        """
        form = EventForm({'location_area': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('location_area', form.errors.keys())
        self.assertEqual(form.errors['location_area'][0],
                         'This field is required.')

    def test_event_location_time_is_required(self):
        """
        Tests if the location_time Field in the Event Form requires an entry
        Pass: Entry required
        """
        form = EventForm({'location_time': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('location_time', form.errors.keys())
        self.assertEqual(form.errors['title'][0], 'This field is required.')

    def test_event_location_online_is_not_required(self):
        """
        Tests if the online Field in the Event Form does not require an entry
        Pass: No entry required
        """
        form = EventForm({'title': 'Watching Squid Game!',
                          'category': 'CIN',
                          'summary': 'Watching on Netflix!',
                          'location_area': 'Meeting at Charlies place!',
                          'location_time': '2022-12-14 12:00:00+00:00'})
        self.assertTrue(form.is_valid())

    def test_fields_are_explicit_in_form_metaclass(self):
        """
        Tests if the Meta Declaration in forms.py contains all required fields
        Pass: No entry required
        """
        form = EventForm()
        self.assertEqual(form.Meta.fields, ('title', 'category', 'summary',
                                            'location_area', 'location_online',
                                            'location_time'))


class TestBrowseForm(TestCase):
    """
    Tests for BrowseForm, which is used for Filtering/Searching Events on
    the Browse Page
    """

    def test_browse_searchstring_is_not_required(self):
        """
        Tests if the searchstring Field in the Browse Form does not require
        an entry
        Pass: No entry required
        """
        form = BrowseForm({'online': 'True',
                           'offline': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_online_is_not_required(self):
        """
        Tests if the online Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'offline': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_offline_is_not_required(self):
        """
        Tests if the offline Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_dining_is_not_required(self):
        """
        Tests if the dining Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'offline': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_cinema_is_not_required(self):
        """
        Tests if the cinema Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'offline': 'True',
                           'dining': 'True',
                           'gaming': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_gaming_is_not_required(self):
        """
        Tests if the gaming Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'offline': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'sports': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_sports_is_not_required(self):
        """
        Tests if the sports Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'offline': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'camping': 'True'})
        self.assertTrue(form.is_valid())

    def test_browse_camping_is_not_required(self):
        """
        Tests if the camping Field in the Browse Form does not require an entry
        Pass: No entry required
        """
        form = BrowseForm({'searchstring': 'Netflix',
                           'online': 'True',
                           'offline': 'True',
                           'dining': 'True',
                           'cinema': 'True',
                           'gaming': 'True',
                           'sports': 'True'})
        self.assertTrue(form.is_valid())

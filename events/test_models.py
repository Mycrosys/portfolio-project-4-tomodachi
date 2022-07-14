from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event


class TestModels(TestCase):
    """
    Testing the Model and its methods
    """

    def setUp(self):
        """
        Setup Class for all Tests in TestModels
        """
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.client.login(username='testuser', password='12345')

    def tearDown(self):
        """
        Teardown Class for all Tests in TestModels
        (Cleans up the setup)
        """
        self.client.logout()
        self.user.delete()

    def test_location_online_defaults_to_false(self):
        """
        Tests if location_online will be false if no value
        is given upon creation of the Model
        """

        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        self.assertFalse(event.location_online)

    def test_item_string_method_returns_name(self):
        """
        Tests if method returns the title of the Event
        """

        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        self.assertEqual(str(event), 'Watching Squid Game!')

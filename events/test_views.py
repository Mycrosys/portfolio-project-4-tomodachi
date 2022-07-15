from django.test import TestCase
from django.contrib.auth.models import User
from .models import Event


class TestViewsPages(TestCase):
    """
    Tests for Views, which are used for routing
    to the correct link and using the correct templates
    """
    def setUp(self):
        """
        Setup Method for all Tests in TestViewsPages
        """
        # Create the User so all Pages are available
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')

    def tearDown(self):
        """
        Teardown Method for all Tests in TestViewsPages
        (Cleans up the setup)
        """
        self.user.delete()

    def test_get_home_page(self):
        """
        Tests if the correct template for the Index Page is
        used and links up fine.
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_register_page(self):
        """
        Tests if the correct template for the Register Account
        Page is used and links up fine.
        """
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/signup.html')

    def test_get_login_page(self):
        """
        Tests if the correct template for the Login
        Page is used and links up fine.
        """
        # Needs to be logged out so this page is available
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_get_logout_page(self):
        """
        Tests if the correct template for the Logout
        Page is used and links up fine.
        """
        # Needs to be logged in so this page is available
        self.client.login(username='testuser', password='12345')
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/logout.html')

    def test_get_my_events_page(self):
        """
        Tests if the correct template for the My Events
        Page is used and links up fine.
        """
        response = self.client.get('/my_events/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_events.html')

    def test_get_create_events_page(self):
        """
        Tests if the correct template for the Create Event
        Page is used and links up fine.
        """
        response = self.client.get('/create_event/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_event.html')

    def test_get_browse_events_page(self):
        """
        Tests if the correct template for the Browse Event
        Page is used and links up fine.
        """
        response = self.client.get('/browse_event/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'browse_event.html')


class TestViewsActions(TestCase):
    """
    Tests for Actions related to creating, modifying, joining,
    leaving and deleting events.
    """

    def setUp(self):
        """
        Setup Method for all Tests in TestViewsActions
        """
        # Create a testuser and log in. This is required for
        # many operations
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.client.login(username='testuser', password='12345')

    def tearDown(self):
        """
        Teardown Method for all Tests in TestViewsActions
        (Cleans up the setup)
        """
        # Logs out the testuser and deletes it from the test
        # Database
        self.client.logout()
        self.user.delete()

    def test_can_browse_events_with_filter_no_events_returned(self):
        """
        Tests if the Filter in Browse Events works correctly
        """
        # Create a test Event in the Database
        Event.objects.create(title='Watching Squid Game!',
                                   category='CIN',
                                   summary='Watching on Netflix!',
                                   location_area='Meeting at Charlies!',
                                   location_time='2022-12-14 12:00:00+00:00',
                                   author=self.user)
        # Post Form with settings that should not return any results
        response = self.client.post('/browse_event/',
                                    {'searchstring': 'Netflix',
                                     'online': 'False',
                                     'offline': 'False',
                                     'dining': 'False',
                                     'cinema': 'False',
                                     'gaming': 'False',
                                     'sports': 'False',
                                     'camping': 'False'})
        self.assertEqual(response.status_code, 200)
        event_list = response.context['event_list']
        self.assertEqual(len(event_list), 0)

    def test_can_browse_events_with_filter_event_returned(self):
        """
        Tests if the Filter in Browse Events works correctly
        """
        # Create a test Event in the Database
        Event.objects.create(title='Watching Squid Game!',
                                   category='CIN',
                                   summary='Watching on Netflix!',
                                   location_area='Meeting at Charlies!',
                                   location_time='2022-12-14 12:00:00+00:00',
                                   author=self.user)
        # Post Form with settings that should return one results
        response = self.client.post('/browse_event/',
                                    {'searchstring': 'Netflix',
                                     'online': 'False',
                                     'offline': 'True',
                                     'dining': 'False',
                                     'cinema': 'True',
                                     'gaming': 'False',
                                     'sports': 'False',
                                     'camping': 'False'})
        self.assertEqual(response.status_code, 200)
        event_list = response.context['event_list']
        self.assertEqual(len(event_list), 1)

    def test_get_modify_event_page(self):
        """
        Tests if the correct template for the Modify Event
        Page is used and it linking up fine.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Enter Modify Page of the created Event
        response = self.client.get(f'/edit/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_event.html')

    def test_can_modify_event(self):
        """
        Tests if the author of an Event can modify his own Event
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Post Form with updated Title
        response = self.client.post(f'/edit/{event.id}/',
                                    {'title': 'Netflix Watchparty!',
                                     'category': 'CIN',
                                     'summary': 'Watching on Netflix!',
                                     'location_area': 'Meeting at Charlies!',
                                     'location_time':
                                     '2022-12-14 12:00:00+00:00'})
        self.assertRedirects(response, '/my_events/')
        updated_event = Event.objects.get(id=event.id)
        self.assertEqual(updated_event.title, 'Netflix Watchparty!')

    def test_can_not_modify_event_if_not_author(self):
        """
        Tests if you can not modify an Event if you are not
        its author.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        # Try to update the Event created by another User
        response = self.client.post(f'/edit/{event.id}/',
                                    {'title': 'Netflix Watchparty!',
                                     'category': 'CIN',
                                     'summary': 'Watching on Netflix!',
                                     'location_area': 'Meeting at Charlies!',
                                     'location_time':
                                     '2022-12-14 12:00:00+00:00'})
        self.assertRedirects(response, '/my_events/')
        updated_event = Event.objects.get(id=event.id)
        self.assertNotEqual(updated_event.title, 'Netflix Watchparty!')

    def test_can_not_modify_event_if_submission_invalid(self):
        """
        Tests if you can not modify an Event if you are not
        its author.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Invalid Submission Form because the summary Field is left empty
        response = self.client.post(f'/edit/{event.id}/',
                                    {'title': 'Netflix Watchparty!',
                                     'category': 'CIN',
                                     'summary': '',
                                     'location_area': 'Meeting at Charlies!',
                                     'location_time':
                                     '2022-12-14 12:00:00+00:00'})
        self.assertRedirects(response, '/my_events/')
        updated_event = Event.objects.get(id=event.id)
        self.assertNotEqual(updated_event.title, 'Netflix Watchparty!')

    def test_get_event_detail_page(self):
        """
        Tests if the correct template for the Event Detail
        Page is used and it linking up fine.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        response = self.client.get(f'/event/{event.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'event_detail.html')

    def test_can_delete_event(self):
        """
        Tests if the created Event is being deleted.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        response = self.client.get(f'/delete/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # get the existing events and check if there are none
        existing_events = Event.objects.filter(id=event.id)
        self.assertEqual(len(existing_events), 0)

    def test_can_not_delete_event_if_not_author(self):
        """
        Tests if the created Event can be deleted if you
        are not the author.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        response = self.client.get(f'/delete/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # get the existing events and check if there is still
        # one event in it
        existing_events = Event.objects.filter(id=event.id)
        self.assertEqual(len(existing_events), 1)

    def test_can_create_event(self):
        """
        Tests if an Event can be created with the create_event Page.
        """
        response = self.client.post('/create_event/',
                                    {'title': 'Watching Squid Game!',
                                     'category': 'CIN',
                                     'summary': 'Watching on Netflix!',
                                     'location_area': 'Meeting at Charlies!',
                                     'location_time':
                                     '2022-12-14 12:00:00+00:00'})
        self.assertRedirects(response, '/my_events/')

        # get the existing events and check if it contains 1 Event
        existing_events = Event.objects.all()
        self.assertEqual(len(existing_events), 1)

        # Compare the amount of Attendees which should now be 1
        # because the view auto-adds the creator als attendee
        self.assertEqual(existing_events[0].attendees.count(), 1)

    def test_can_not_create_event_if_invalid_submission(self):
        """
        Tests if an Event can be created with the create_event Page.
        """
        # Create a test Event via the Form Submission
        # Title is left empty which leads to invalid submission
        response = self.client.post('/create_event/',
                                    {'title': '',
                                     'category': 'CIN',
                                     'summary': 'Watching on Netflix!',
                                     'location_area': 'Meeting at Charlies!',
                                     'location_time':
                                     '2022-12-14 12:00:00+00:00'})
        self.assertRedirects(response, '/my_events/')

        # get the existing events and check if it contains 0 Events
        existing_events = Event.objects.all()
        self.assertEqual(len(existing_events), 0)

    def test_can_join_event(self):
        """
        Tests if you can join an Event.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        response = self.client.get(f'/join/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # Compare the amount of Attendees which should now be 1
        self.assertEqual(event.attendees.count(), 1)

    def test_can_not_join_event_if_already_attendee(self):
        """
        Tests if you can join an Event if you are already
        are an Attendee.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        # Add one Attendee for a total of 1
        event.attendees.add(self.user)
        response = self.client.get(f'/join/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # Compare the amount of Attendees which should still be 1
        self.assertEqual(event.attendees.count(), 1)

    def test_can_leave_event(self):
        """
        Tests if you can leave an Event.
        """
        # Create a test Event in the Database
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        event.attendees.add(self.user)
        response = self.client.get(f'/leave/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # Compare the amount of Attendees which should now be 0
        self.assertEqual(event.attendees.count(), 0)

    def test_can_not_leave_event_if_not_attendee(self):
        """
        Tests if you can leave an Event if you are not an Attendee
        """
        event = Event.objects.create(title='Watching Squid Game!',
                                     category='CIN',
                                     summary='Watching on Netflix!',
                                     location_area='Meeting at Charlies!',
                                     location_time='2022-12-14 12:00:00+00:00',
                                     author=self.user)
        # Logout current user and log in with a second one
        self.client.logout()
        self.user = User.objects.create_user(username='testuser2',
                                             password='12346')
        self.client.login(username='testuser2', password='12346')
        response = self.client.get(f'/leave/{event.id}/')
        self.assertRedirects(response, '/my_events/')

        # Compare the amount of Attendees which should still be 0
        self.assertEqual(event.attendees.count(), 0)

from django.urls import path
from . import views


urlpatterns = [
    # Home/Index Page
    path('', views.EventList.as_view(), name='home'),

    # Event Detail Page
    path('event/<int:pk>/', views.EventDetail.as_view(),
         name='event_detail'),

    # Event Create Page
    path('create_event/', views.EventCreate.as_view(), name='create_event'),

    # My Events Page
    path('my_events/', views.EventMy.as_view(), name='my_events'),

    # Browse Event Page
    path('browse_event/', views.EventBrowse.as_view(), name='browse_event'),

    # Leave Event Page (redirects back to my events after code execution)
    path('leave/<int:pk>/', views.EventRemoveAttendee.as_view(),
         name='leave_event'),

    # Join Event Page (redirects back to my events after code execution)
    path('join/<int:pk>/', views.EventAddAttendee.as_view(),
         name='join_event'),

    # Delete Event Page (redirects back to my events after code execution)
    path('delete/<int:pk>/', views.EventDelete.as_view(),
         name='delete_event'),

    # Modify Event Page
    path('edit/<int:pk>/', views.EventEdit.as_view(),
         name='edit_event'),
]

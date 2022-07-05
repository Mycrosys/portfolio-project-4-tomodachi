from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('event/<slug:slug>/', views.EventDetail.as_view(),
         name='event_detail'),
    path('create_event/', views.EventCreate.as_view(), name='create_event'),
    path('my_events/', views.EventMy.as_view(), name='my_events'),
    path('leave/<slug:slug>/', views.EventRemoveAttendee.as_view(),
         name='leave_event'),
    path('join/<slug:slug>/', views.EventAddAttendee.as_view(),
         name='join_event'),
]

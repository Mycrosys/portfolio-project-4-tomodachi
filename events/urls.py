from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('event/<int:pk>/', views.EventDetail.as_view(),
         name='event_detail'),
    path('create_event/', views.EventCreate.as_view(), name='create_event'),
    path('my_events/', views.EventMy.as_view(), name='my_events'),
    path('leave/<int:pk>/', views.EventRemoveAttendee.as_view(),
         name='leave_event'),
    path('join/<int:pk>/', views.EventAddAttendee.as_view(),
         name='join_event'),
    path('delete/<int:pk>/', views.EventDelete.as_view(),
         name='delete_event'),
    path('edit/<int:pk>/', views.EventEdit.as_view(),
         name='edit_event'),
]

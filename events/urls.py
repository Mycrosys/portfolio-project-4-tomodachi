from django.urls import path
from . import views


urlpatterns = [
    path('', views.EventList.as_view(), name='home'),
    path('event/<slug:slug>/', views.EventDetail.as_view(),
         name='event_detail'),
    path('create_event/', views.EventCreate.as_view(), name='create_event'),
]

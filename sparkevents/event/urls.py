from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/<int:event_id>/edit/', views.event_edit, name='event_edit'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),
    path('registration_success/', views.registration_success, name='registration_success'),
    path('register/', views.register, name='register'),
    path('registered_events/', views.registered_events, name='registered_events'),
    path('events/<int:event_id>/cancel_registration/', views.cancel_registration, name='cancel_registration'),

    
]

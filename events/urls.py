from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('events/', views.event_list, name='event_list'),
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:event_id>/update/', views.event_update, name='event_update'),
    path('events/<int:event_id>/delete/', views.event_delete, name='event_delete'),
    path('dashboard/', views.dashboard, name='dashboard'),  
]

from django.urls import path
from . import views
from .views import signup_view, login_view, logout_view, dashboard_view

urlpatterns = [
    path('events/', views.event_list, name='event_list'),
    path('events/create/', views.event_create, name='event_create'),
    path('events/<int:pk>/edit/', views.event_update, name='event_update'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/', views.event_detail, name='event_detail'), 
    path("accounts/dashboard/view/", dashboard_view, name="dashboard_view"),  # ✅ comma added
    path('dashboard/', dashboard_view, name='dashboard'),  # ✅
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
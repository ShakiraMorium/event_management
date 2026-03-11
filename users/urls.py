from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("signup/", views.signup_view, name="signup"),
    path("activate/<uidb64>/<token>/", views.activate_view, name="activate"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),

    # Dashboard
    path("dashboard/view/", views.dashboard_view, name="dashboard_view"),
    path("dashboard/", views.dashboard_view, name="dashboard"),
#    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
#    path("organizer-dashboard/", views.organizer_dashboard, name="organizer_dashboard"),
#    path("participant-dashboard/", views.participant_dashboard, name="participant_dashboard"),  
]
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from .forms import SignupForm
from  users.models import Profile
from django.utils import timezone
from events.models import Event, Participant 
from django.contrib.auth.forms import UserCreationForm

# --------------------------
# Signup with activation
# --------------------------
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            
            # Assign default group
            group = Group.objects.get(name="Participant")
            user.groups.add(group)

            Profile.objects.create(user=user)

            login(request, user)
            return redirect("dashboard")

    else:
        form = UserCreationForm()

    return render(request, "users/signup.html", {"form": form})
# --------------------------

# Login / Logout
# --------------------------
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect(request.GET.get("next", "dashboard"))

    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')

def activate_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('dashboard')
    else:
        return render(request, 'dashboard_view')



# --------------------------
# Dashboard Redirect
# --------------------------



@login_required
def dashboard_view(request):
    user = request.user

    # Safe profile handling
    profile, created = Profile.objects.get_or_create(user=user)

    # Admin dashboard
    if user.groups.filter(name="Admin").exists():
        context = {
            "profile": profile,
            "total_users": User.objects.count(),
            "total_events": Event.objects.count(),
        }
        return render(request, "users/admin_dashboard.html", context)

    # Organizer dashboard
    elif user.groups.filter(name="Organizer").exists():
        events = Event.objects.filter(organizer=user).order_by("-date")
        today = timezone.now().date()
        todays_events = events.filter(date=today)
        upcoming_events = events.filter(date__gt=today)
        past_events = events.filter(date__lt=today)
        active_filter = request.GET.get("filter", "all")
        if active_filter == "today":
            events_filtered = todays_events
        elif active_filter == "upcoming":
            events_filtered = upcoming_events
        elif active_filter == "past":
            events_filtered = past_events
        else:
            events_filtered = events
        context = {
            "profile": profile,
            "events": events_filtered,
            "total_events": events.count(),
            "todays_events": todays_events,
            "upcoming_events_count": upcoming_events.count(),
            "past_events_count": past_events.count(),
            "active_filter": active_filter,
        }
        return render(request, "users/organizer_dashboard.html", context)

    # Participant dashboard
    elif user.groups.filter(name="Participant").exists():
        participant_events = Event.objects.filter(participant__user=user).order_by("-date")
        today = timezone.now().date()
        upcoming_events = participant_events.filter(date__gte=today)
        past_events = participant_events.filter(date__lt=today)
        context = {
            "profile": profile,
            "events": upcoming_events,
            "upcoming_events_count": upcoming_events.count(),
            "past_events_count": past_events.count(),
        }
        return render(request, "users/participant_dashboard.html", context)

    # fallback to login
    return redirect("login")
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.contrib.auth.models import User, Group
from users.models import Profile
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail


# -------------------------------
# AUTHENTICATION VIEWS
# -------------------------------

def signup_view(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            domain = get_current_site(request).domain

            subject = "Activate Your Account"

            message = render_to_string(
                "registration/activation_email.html",
                {
                    "user": user,
                    "domain": domain,
                    "uid": uid,
                    "token": token,
                },
            )

            send_mail(subject, message, "admin@yourevents.com", [user.email])

            return render(request, "registration/activation_sent.html")

    else:
        form = UserCreationForm()

    return render(request, "registration/signup.html", {"form": form})


def login_view(request):

    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")

    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


def logout_view(request):

    if request.method == "POST":
        logout(request)
        return redirect("login")


# -------------------------------
# ROLE CHECK FUNCTIONS
# -------------------------------

def is_admin(user):
    return user.groups.filter(name="Admin").exists()


def is_organizer(user):
    return user.groups.filter(name="Organizer").exists()


# -------------------------------
# HOME PAGE
# -------------------------------

def home_view(request):

    today = timezone.now().date()

    upcoming_events = Event.objects.select_related(
        "category"
    ).prefetch_related(
        "participants"
    ).filter(
        date__gte=today
    ).order_by("date", "time")

    return render(
        request,
        "events/home.html",
        {
            "upcoming_events": upcoming_events
        },
    )


# -------------------------------
# EVENT LIST + SEARCH
# -------------------------------

def event_list(request):

    search = request.GET.get("q", "")

    events = Event.objects.select_related("category")

    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )

    return render(
        request,
        "events/event_list.html",
        {
            "events": events,
            "search": search,
        },
    )


# -------------------------------
# EVENT DETAIL
# -------------------------------

def event_detail(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    return render(
        request,
        "events/event_detail.html",
        {"event": event},
    )


# -------------------------------
# CREATE EVENT
# -------------------------------

@login_required
@user_passes_test(is_organizer)
def event_create(request):

    form = EventForm(request.POST or None, request.FILES or None)

    if request.method == "POST":

        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user
            event.save()

            return redirect("event_list")

    return render(
        request,
        "events/event_form.html",
        {"form": form},
    )


# -------------------------------
# UPDATE EVENT
# -------------------------------

@login_required
@user_passes_test(is_organizer)
def event_update(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        return redirect("event_list")

    return render(
        request,
        "events/event_form.html",
        {
            "form": form,
            "title": "Update Event",
        },
    )


# -------------------------------
# DELETE EVENT
# -------------------------------

@login_required
@user_passes_test(is_admin)
def event_delete(request, event_id):

    event = get_object_or_404(Event, id=event_id)

    if request.method == "POST":
        event.delete()
        return redirect("event_list")

    return render(
        request,
        "events/event_confirm_delete.html",
        {"event": event},
    )


# -------------------------------
# RSVP SYSTEM
# -------------------------------

@login_required
def rsvp_event(request, pk):

    event = get_object_or_404(Event, id=pk)

    if request.user not in event.participants.all():
        event.participants.add(request.user)

    return redirect("event_detail", event_id=pk)


# -------------------------------
# DASHBOARD
# -------------------------------

@login_required
@login_required
def dashboard_view(request):
    user = request.user

    # Get or create profile
    profile, created = Profile.objects.get_or_create(user=user)

    # ----------------------
    # ADMIN DASHBOARD
    # ----------------------
    if user.groups.filter(name="Admin").exists():
        context = {
            "profile": profile,
            "total_users": User.objects.count(),
            "total_events": Event.objects.count(),
        }
        return render(request, "users/admin_dashboard.html", context)

    # ----------------------
    # ORGANIZER DASHBOARD
    # ----------------------
    elif user.groups.filter(name="Organizer").exists():

        events = Event.objects.filter(organizer=user).order_by("-date")

        # ----------------------
        # SET TODAY, FILTERS, STATS HERE
        # ----------------------
        today = timezone.now().date()
        todays_events = events.filter(date=today)
        upcoming_events_count = events.filter(date__gt=today).count()
        past_events_count = events.filter(date__lt=today).count()

        context = {
            "profile": profile,
            "events": events,
            "total_events": events.count(),
            "todays_events": todays_events,
            "upcoming_events_count": upcoming_events_count,
            "past_events_count": past_events_count,
        }

        return render(request, "users/organizer_dashboard.html", context)

    # ----------------------
    # PARTICIPANT DASHBOARD
    # ----------------------
    elif user.groups.filter(name="Participant").exists():

        participant_events = Event.objects.filter(participant__user=user).order_by("-date")

        today = timezone.now().date()
        todays_events = participant_events.filter(date=today)
        upcoming_events_count = participant_events.filter(date__gt=today).count()
        past_events_count = participant_events.filter(date__lt=today).count()

        context = {
            "profile": profile,
            "events": participant_events,
            "todays_events": todays_events,
            "upcoming_events_count": upcoming_events_count,
            "past_events_count": past_events_count,
        }

        return render(request, "users/participant_dashboard.html", context)

    # ----------------------
    # fallback
    # ----------------------
    return redirect("login")
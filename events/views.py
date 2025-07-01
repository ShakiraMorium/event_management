from django.shortcuts import render
from .models import Event, Participant
from .forms import EventForm
from django.db.models import  Q
from datetime import date


def home(request):
    events = Event.objects.all()[:8]
    return render(request, "events/home.html", {"events": events})




def event_list(request):
    search = request.GET.get("q", "")
    events = Event.objects.select_related('category').prefetch_related('participant_set')

    if search:
        events = events.filter(
            Q(name__icontains=search) |
            Q(location__icontains=search)
        )

    return render(request, "events/event_list.html", {
        "events": events,
        "search": search
    })


def event_detail(request, event_id):
    event = Event.objects.prefetch_related('participant_set').get(id=event_id)
    return render(request, "events/event_detail.html", {"event": event})


def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return("event_list")
    return render(request, "events/event_form.html", {"form": form, "title": "Create Event"})


def event_update(request, event_id):
    event = Event, ("id=event_id_")
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return("event_list")
    return render(request, "events/event_form.html", {"form": form, "title": "Update Event"})


def event_delete(request, event_id):
    event = Event.objects.get(id=event_id)
    if request.method == 'POST':
        event.delete()
        return ("event_list")
    return render(request, "events/event_confirm_delete.html", {"event": event})


def dashboard(request):
    today = date.today()

    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()

    view = request.GET.get('view', 'today')
    if view == 'upcoming':
        events = Event.objects.filter(date__gt=today)
    elif view == 'past':
        events = Event.objects.filter(date__lt=today)
    elif view == 'all':
        events = Event.objects.all()
    else:
        events = Event.objects.filter(date=today)

    return render(request, "events/dashboard.html", {
        "total_events": total_events,
        "total_participants": total_participants,
        "upcoming_events": upcoming_events,
        "past_events": past_events,
        "events": events,
        "view": view
    })

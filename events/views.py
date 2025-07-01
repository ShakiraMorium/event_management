from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from datetime import date


def home(request):
    event = Event.objects.all() 
    context = {
        'event': event}
    return render(request, "events/home.html", context)
    








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
    form = EventForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'events/event_form.html', {'form': form})


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


# def dashboard(request):
#     today = timezone.now().date()

#     # Stats
#     total_events = Event.objects.count()
#     total_participants = Participant.objects.count()
#     upcoming_events = Event.objects.filter(date__gt=today)
#     past_events = Event.objects.filter(date__lt=today)
#     todays_events = Event.objects.filter(date=today)

#     # Stat filter
#     stat_filter = request.GET.get('filter', 'today')
#     if stat_filter == 'all':
#         filtered_events = Event.objects.all()
#     elif stat_filter == 'upcoming':
#         filtered_events = upcoming_events
#     elif stat_filter == 'past':
#         filtered_events = past_events
#     else:
#         filtered_events = todays_events  # Default to today's events

#     context = {
#         'total_events': total_events,
#         'total_participants': total_participants,
#         'upcoming_events_count': upcoming_events.count(),
#         'past_events_count': past_events.count(),
#         'todays_events': todays_events,
#         'events': filtered_events,
#         'active_filter': stat_filter,
#     }
#     return render(request, 'events/dashboard.html', context)

# def dashboard(request):
#     today = timezone.now().date()
#     events = Event.objects.all()

#     context = {
#         'total_participants': Participant.objects.count(),
#         'total_events': events.count(),
#         'upcoming_events_count': events.filter(date__gt=today).count(),
#         'past_events_count': events.filter(date__lt=today).count(),
#         'todays_events': events.filter(date=today),
#     }
#     return render(request, 'events/dashboard.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Participant, Category
from .forms import EventForm, ParticipantForm, CategoryForm
from datetime import date

# Dashboard view
def dashboard(request):
    total_events = Event.objects.count()
    total_participants = Participant.objects.count()
    today = date.today()

    upcoming_events = Event.objects.filter(date__gt=today).count()
    past_events = Event.objects.filter(date__lt=today).count()
    todays_events = Event.objects.filter(date=today)

    return render(request, 'events/dashboard.html', {
        'total_events': total_events,
        'total_participants': total_participants,
        'upcoming_events': upcoming_events,
        'past_events': past_events,
        'todays_events': todays_events,
    })

# You can include the CRUD views from earlier here too

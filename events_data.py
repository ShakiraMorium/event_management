import os

import django
from events.models import Event, Category, Participant
from faker import Faker
import random
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()
fake = Faker()

from events.models import Category, Event, Participant
def create_categories(n=5):
    categories = []
    for _ in range(n):
        cat = Category.objects.create(
            name=fake.unique.word().capitalize(),
            description=fake.sentence()
        )
        categories.append(cat)
    return categories

def create_events(categories, n=15):
    events = []
    for _ in range(n):
        evt = Event.objects.create(
            name=fake.unique.catch_phrase(),
            description=fake.text(max_nb_chars=200),
            date=fake.date_between(start_date='-5d', end_date='+15d'),
            time=fake.time(),
            location=fake.city(),
            category=random.choice(categories)
        )
        events.append(evt)
    return events

def create_participants(events, n=30):
    for _ in range(n):
        participant = Participant.objects.create(
            name=fake.name(),
            email=fake.unique.email()
        )
        participant.events.set(random.sample(events, random.randint(1, 3)))

def run():
    categories = create_categories()
    events = create_events(categories)
    create_participants(events)
    print("Fake data created successfully!")

if __name__ == "__main__":
    run()

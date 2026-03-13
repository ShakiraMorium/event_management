import os
import django
from faker import Faker
import random
from events.models import Organizer, Event, EventDetail, Category

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()


def populate_db():
    fake = Faker()

    # Create Event Categories
    categories = [Category.objects.create(
        name=fake.word().capitalize(),
        description=fake.paragraph()
    ) for _ in range(5)]

    print(f"Created {len(categories)} categories.")

    # Create Organizers
    organizers = [Organizer.objects.create(
        name=fake.name(),
        email=fake.email()
    ) for _ in range(10)]

    print(f"Created {len(organizers)} organizers.")

    # Create Events
    events = []
    for _ in range(20):
        event = Event.objects.create(
            category=random.choice(categories),
            title=fake.sentence(),
            description=fake.paragraph(),
            event_date=fake.date_this_year(),
            status=random.choice(['UPCOMING', 'ONGOING', 'COMPLETED']),
            is_active=random.choice([True, False])
        )

        event.organizers.set(random.sample(organizers, random.randint(1, 3)))
        events.append(event)

    print(f"Created {len(events)} events.")

    # Create Event Details
    for event in events:
        EventDetail.objects.create(
            event=event,
            organizers=", ".join([org.name for org in event.organizers.all()]),
            priority=random.choice(['H', 'M', 'L']),
            notes=fake.paragraph()
        )

    print("Populated EventDetails for all events.")
    print("Database populated successfully!")
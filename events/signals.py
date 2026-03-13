from django.db.models.signals import post_save, pre_save, m2m_changed, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from events.models import Event

@receiver(m2m_changed, sender=Event.assigned_to.through)
def notify_employees_on_event_creation(sender, instance, action, **kwargs):
    if action == "post_add":
        print(instance, instance.assigned_to.all())


        assigned_emails = [emp.email for emp in instance.assigned_to.all()]
        print("Checking....", assigned_emails)

    send_mail(
        "New Event Assigned",
        f"You have been assigned to the event: {instance.title}",
        "slashupdates@gmail.com",
        assigned_emails,
        fail_silently=False,
    )


@receiver(post_delete, sender=Event)
def delete_associate_event_details(sender, instance, **kwargs):
    if instance.details:
       instance.details.delete()
print("Event details deleted successfully")

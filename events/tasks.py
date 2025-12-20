from celery import shared_task
from django.utils import timezone
from django.core.mail import send_mail
from .models import Event
from django.conf import settings


@shared_task
def update_past_events_status():
    past_events = Event.objects.filter(date__lt=timezone.now().date(), status="active")
    count = past_events.update(status="past")
    return f"Updated {count} events to past status."


# def update_past_events_status():
#     past_events = []
#     events = Event.objects.all()
#     for event in events:
#         if event.is_passed():
#             past_events.append(event)
#     return f"Updated {past_events} events to past status."


@shared_task
def send_ticket_email(to_email, ticket_info):
    """
    Sends an email containing ticket information.
    """
    subject = "Your EventHub Ticket"
    message = f"""
        Hello!\n\nHere are your ticket details:\n\n{ticket_info}\n\nPresent this email at the event entrance.
        """
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])
    # send_mail(subject, message, from_email, ['crazynegin@gmail.com'])

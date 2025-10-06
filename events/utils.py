from django.core.mail import send_mail
from django.conf import settings

def send_ticket_email(user_email, ticket_details):
    subject = 'Your Ticket Purchase Confirmation'
    message = f'Thank you for your purchase!\n\nTicket Details:\n{ticket_details}'
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
        fail_silently=False,
    )

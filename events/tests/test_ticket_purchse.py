import pytest
from django.urls import reverse

from events.tests.factories import EventFactory, UserFactory
from events.models import Ticket

@pytest.mark.django_db
def test_buy_ticket_success(client):
    user = UserFactory(is_attendee=True)
    user.save()
    event = EventFactory(tickets_available=5)
    event.save()
    
    client.force_login(username=user.username, password="password123")

    response = client.post(
        reverse("buy", args=[event.id]),
        {"quantity": 2},
        follow=True,
    )
    print("status", response.status_code)
    print("content:", response.content.decode()[:500])
    
    print("tickets count:", Ticket.objects.filter(event=event).count())


    event.refresh_from_db()

    assert response.status_code == 200
    assert event.tickets_sold() == 2
    assert event.tickets_remaining() == 3

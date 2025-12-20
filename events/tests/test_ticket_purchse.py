import pytest
from django.urls import reverse

from events.tests.factories import EventFactory, UserFactory
from events.models import Ticket

@pytest.mark.django_db
def test_buy_ticket_success(client):
    user = UserFactory(is_attendee=True)  # password handled by factory
    event = EventFactory(tickets_available=5)
    
    client.force_login(user)

    response = client.post(
        reverse("buy", args=[event.id]),
        {"quantity": 2},
        follow=True,
    )

    event.refresh_from_db()

    assert response.status_code == 200
    assert event.tickets_sold() == 2
    assert event.tickets_remaining() == 3

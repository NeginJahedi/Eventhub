from django.urls import reverse
import pytest
from events.tests.factories import EventFactory, UserFactory


@pytest.mark.django_db
def test_buy_ticket_success(client):
    user = UserFactory()
    event = EventFactory(total_tickets=5)

    client.login(username=user.username, password="password123")

    response = client.post(reverse("buy_ticket", args=[event.id]), {"quantity": 2})

    event.refresh_from_db()
    assert response.status_code == 200
    assert event.tickets_remaining() == 3

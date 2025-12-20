import pytest
import threading
from django.urls import reverse
from django.test import Client
from events.models import Ticket
from events.tests.factories import EventFactory, UserFactory


@pytest.mark.django_db(transaction=True)
def test_no_oversell_under_concurrency():
    event = EventFactory(tickets_available=1)
    users = [UserFactory() for _ in range(2)]

    def attempt_purchase(user):
        client = Client()
        client.force_login(user)
        client.post(
            reverse("buy", args=[event.id]),
            {"quantity": 1},
            follow=True,
        )

    threads = [threading.Thread(target=attempt_purchase, args=(user,)) for user in users]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    event.refresh_from_db()
    assert event.tickets_sold() == 1
    assert event.tickets_remaining() == 0

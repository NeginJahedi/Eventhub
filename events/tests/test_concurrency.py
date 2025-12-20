import pytest
import threading
from django.db import transaction
from django.urls import reverse
from events.tests.factories import EventFactory, UserFactory
from django.test import Client

@pytest.mark.django_db(transaction=True)
def test_no_oversell_under_concurrency():
    event = EventFactory(total_tickets=1)
    users = [UserFactory() for _ in range(2)]

    def attempt_purchase(user):
        client = Client()
        client.login(username=user.username, password="password123")
        client.post(
            reverse("buy_ticket", args=[event.id]),
            {"quantity": 1}
        )

    threads = [
        threading.Thread(target=attempt_purchase, args=(u,))
        for u in users
    ]

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    event.refresh_from_db()
    assert event.tickets_remaining() == 0
    assert event.tickets_sold() == 1

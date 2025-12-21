from django.db import connection
import pytest
import threading
from django.urls import reverse
from django.test import Client
from events.models import Ticket
from events.tests.factories import EventFactory, UserFactory


@pytest.mark.django_db(transaction=True)
def test_no_oversell_under_concurrency(live_server):
    # Create an event with only 1 ticket available
    event = EventFactory(tickets_available=1)

    # Create 2 users
    users = [UserFactory() for _ in range(2)]

    # Make sure users have a known password
    for user in users:
        user.set_password("password123")
        user.save()

    # Function each thread will run

    def attempt_purchase(user):
        client = Client()
        client.force_login(user, backend='django.contrib.auth.backends.ModelBackend')
        client.post(f"{live_server.url}{reverse('buy', args=[event.id])}", {"quantity": 1}, follow=True)
        connection.close()  # ensure DB connections are closed per thread

    # Create threads for each user
    threads = [threading.Thread(target=attempt_purchase, args=(user,)) for user in users]

    # Start all threads
    for t in threads:
        t.start()

    # Wait for all threads to finish
    for t in threads:
        t.join()

    # Refresh from DB to get latest ticket count
    event.refresh_from_db()

    # Only 1 ticket should be sold
    assert event.tickets_sold() == 1
    assert event.tickets_remaining() == 0

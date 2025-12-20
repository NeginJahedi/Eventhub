import pytest
from events.tests.factories import EventFactory, TicketFactory


@pytest.mark.django_db
def test_tickets_remaining():
    event = EventFactory(total_tickets=5)
    TicketFactory(event=event, quantity=2)
    TicketFactory(event=event, quantity=1)

    assert event.tickets_remaining() == 2


@pytest.mark.django_db
def test_event_revenue():
    event = EventFactory(price=10)
    TicketFactory(event=event, quantity=3)

    assert event.revenue() == 30

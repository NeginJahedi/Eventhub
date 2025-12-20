import factory
from django.utils import timezone
from events.models import User, Event, Ticket
from decimal import Decimal

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda o: f"{o.username}@test.com")
    password = factory.PostGenerationMethodCall("set_password", "password123")

class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Test Event"
    description = "Test Description"
    location = "Test Location"
    date = factory.LazyFunction(lambda: timezone.now().date())
    price = Decimal("10.00")
    total_tickets = 10
    status = "active"
    organizer = factory.SubFactory(UserFactory)

class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    event = factory.SubFactory(EventFactory)
    attender = factory.SubFactory(UserFactory)
    quantity = 1

import factory
from decimal import Decimal
from django.utils import timezone

from events.models import User, Event, Ticket


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.LazyAttribute(lambda obj: f"{obj.username}@test.com")
    is_attendee = True
    is_organizer = False

    @factory.post_generation
    def password(self, create, extracted, **kwargs):
        pwd = extracted or "password123"
        self.set_password(pwd)
        if create:
            self.save()


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event

    title = "Test Event"
    description = "Test Description"
    category = "arts"
    location = "Test Location"
    date = factory.LazyFunction(lambda: timezone.now().date())
    time = factory.LazyFunction(lambda: timezone.now().time())
    price = Decimal("10.00")
    tickets_available = 10
    status = "active"
    image = factory.django.ImageField(color="blue")

    organizer = factory.SubFactory(
        UserFactory,
        is_organizer=True,
    )


class TicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ticket

    event = factory.SubFactory(EventFactory)
    attender = factory.SubFactory(
        UserFactory,
        is_attendee=True,
    )
    quantity = 1
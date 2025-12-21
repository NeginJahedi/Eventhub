from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from .models import Event, Ticket
from .forms import EventForm, EventsUserCreationForm
from django.http import JsonResponse
import json
from datetime import datetime
from django.contrib import messages
from collections import defaultdict
from .helper import organizer_required, paginate_queryset
from .tasks import send_ticket_email
from django.contrib.auth import login, logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()

N = 10  # number of events on each page
M = 10  # number of tickets on each page


# Create your views here..
def index(request):
    events = Event.objects.all()
    categories = Event.CATEGORY_CHOICES
    category_dict = dict(categories)
    page_obj = paginate_queryset(events, request, N)
    return render(
        request,
        "events/index.html",
        {"page_obj": page_obj, "categories": category_dict.keys},
    )


# Create your views here.
def register_view(request):
    if request.method == "POST":
        # register user
        form = EventsUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    else:
        form = EventsUserCreationForm()
        # show registeration page
    return render(request, "events/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

    else:
        form = AuthenticationForm()
    return render(request, "events/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


@login_required
def create(request):
    if request.method == "POST":
        new_event = EventForm(request.POST, request.FILES)
        # print(request.POST)
        # print(request.FILES)
        if new_event.is_valid():
            # print("form is valid")
            new_event = new_event.save(commit=False)
            new_event.organizer = request.user
            request.user.is_organizer = True
            request.user.save()
            new_event.save()
            return HttpResponseRedirect(
                reverse("index")
            )  # going to change this >> redirect to all events
        else:
            print("form is invalid")
        print(new_event.errors)
    else:
        new_event = EventForm()
    return render(request, "events/create.html", {"form": new_event})


def event_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, "events/event.html", {"event": event})


@login_required
def buy_ticket_view(request, event_id):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("event", args=(event_id,)))

    try:
        quantity = int(request.POST.get("quantity", 0))
    except (TypeError, ValueError):
        messages.warning(request, "Invalid ticket quantity.")
        return HttpResponseRedirect(reverse("event", args=(event_id,)))

    try:
        with transaction.atomic():
            # Lock the event row to avoid oversell under concurrency
            event_obj = Event.objects.select_for_update().get(id=event_id)

            # All reads after lock
            remaining = event_obj.tickets_remaining()

            if event_obj.status == "past":
                messages.warning(request, "Sorry. This event's date has passed.")
                return HttpResponseRedirect(reverse("event", args=(event_id,)))

            if event_obj.status == "canceled":
                messages.warning(request, "Sorry. This event has been canceled.")
                return HttpResponseRedirect(reverse("event", args=(event_id,)))

            if remaining <= 0:
                event_obj.status = "sold_out"
                event_obj.save(update_fields=["status"])
                messages.warning(request, "Sold out! No more tickets available.")
                return HttpResponseRedirect(reverse("event", args=(event_id,)))

            if quantity > remaining:
                messages.warning(request, f"Only {remaining} tickets are remaining.")
                return HttpResponseRedirect(reverse("event", args=(event_id,)))
            
            # Create ticket while inside the transaction
            ticket_bought = Ticket.objects.create(
                event=event_obj, attender=request.user, quantity=quantity
            )
            
            # Update status if this purchase sold out the event
            if remaining - quantity == 0:
                event_obj.status = "sold_out"
                event_obj.save(update_fields=["status"])

        # At this point the transaction has committed.
        # Schedule side-effects to run only after commit to avoid race/visibility issues.
        def _after_commit():
            total_price = quantity * event_obj.price
            ticket_info = (
                f"Event: {event_obj.title}\n"
                f"Date: {event_obj.date}\n"
                f"Location: {event_obj.location}"
            )
            # use Celery task asynchronously — scheduled after commit
            send_ticket_email.delay(request.user.email, ticket_info)
            # no return value needed

        transaction.on_commit(_after_commit)

        total_price = quantity * event_obj.price
        messages.success(request, "Ticket was purchased successfully.")

        return render(
            request,
            "events/reciept.html",
            {"ticket_bought": ticket_bought, "total_price": total_price},
        )

    except Event.DoesNotExist:
        return HttpResponseRedirect(reverse("index"))


def search_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            query = data.get("search_keyword", "")
            category = data.get("category", "")
            start_date = data.get("start_date", "")
            end_date = data.get("end_date", "")
            min_price = data.get("min_price", "")
            max_price = data.get("max_price", "")
            location = data.get("location", "")
            search_results = Event.objects.all()
            # print(search_results)
            if query:
                search_results = search_results.filter(title=query)

            # Filter by category
            if category:
                search_results = search_results.filter(category=category)

            if location:
                search_results = search_results.filter(location=location)

            # Filter by date range
            if start_date and end_date:
                start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
                end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
                search_results = search_results.filter(
                    date__gte=start_date, date__lte=end_date
                )

            # Filter by price range
            if min_price and max_price:
                search_results = search_results.filter(
                    price__gte=float(min_price), price__lte=float(max_price)
                )
            elif min_price:
                search_results = search_results.filter(price__gte=float(min_price))
            elif max_price:
                search_results = search_results.filter(price__lte=float(max_price))

            # Prepare results for frontend
            results = [
                {
                    "id": result.id,
                    "title": result.title,
                    "category": result.category,
                    "date": result.date.strftime("%Y-%m-%d"),
                    "price": str(result.price),
                    "location": result.location,
                    "image_url": result.image.url,
                }
                for result in search_results
            ]
            # results = serialize('json', search_results)

            return JsonResponse({"results": results}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

    return JsonResponse({"error": "Invalid request method"}, status=405)


# @login_required
# def organizer_dashboard(request):
#     organizer = request.user
#     events = organizer.events.all().order_by('-date')

#     total_tickets_sold = 0
#     for event in events:
#         total_tickets_sold += int(event.tickets_sold())
#         total_revenue = (event.price) * event.tickets_sold()
#         # print(total_tickets_sold)
#         # print(total_revenue)

#     return render (request, "events/organizer.html",{
#         "organized_events" : events,
#         "tickets_sold" : total_tickets_sold,
#         "total_revenue" : total_revenue
#     })


@organizer_required
def organizer_dashboard(request):
    organizer = request.user
    events = organizer.events.all().order_by("-date")

    total_tickets_sold = sum(event.tickets_sold() for event in events)
    total_revenue = sum(event.revenue() for event in events)

    # Prepare data for Charts
    sales_data = []
    revenue_data = []
    event_labels = []
    category_data = defaultdict(int)

    for event in events:
        event_labels.append(event.title)
        sales_data.append(event.tickets_sold())
        revenue_data.append(float(event.revenue()))
        category_data[
            event.category
        ] += event.tickets_sold()  # Aggregate category-wise ticket sales

    category_labels = list(category_data.keys())
    category_sales = list(category_data.values())

    return render(
        request,
        "events/organizer.html",
        {
            "organized_events": events,
            "tickets_sold": total_tickets_sold,
            "total_revenue": float(total_revenue),
            "event_labels": event_labels,
            "sales_data": sales_data,
            "revenue_data": revenue_data,
            "category_labels": category_labels,
            "category_sales": category_sales,
        },
    )


@organizer_required
def edit_event_view(request, event_id):
    event = get_object_or_404(Event, id=int(event_id))
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete":
            event.delete()
            return HttpResponseRedirect(reverse("organizer"))

        event_form = EventForm(request.POST, instance=event)
        if request.POST.get("statusChange"):
            event.status = request.POST.get("statusChange")
        if event_form.is_valid():
            event_form.save()
            messages.success(request, "The edits were applied successfully.")
            return HttpResponseRedirect(reverse("event", args=(event_id,)))
        # print(event_form)
        return render(request, "events/edit.html", {"form": event_form, "event": event})
    # print(event)
    else:
        if event.organizer != request.user:
            messages.warning(request, "Only Organizers can edit Events.")
        event_form = EventForm(instance=event)
        return render(request, "events/edit.html", {"form": event_form, "event": event})


@login_required
def filter_view(request):
    try:
        # data = json.loads(request.body)  # Parse JSON from request body
        filter = request.GET.get("status")
        query = request.GET.get("q")

        # search_results = SearchQuerySet().models(Event).all().order_by('-date')
        search_results = Event.objects.all().order_by("-date")
        search_results = search_results.filter(organizer=request.user)

        # print(request.user)
        # print(search_results)
        if query:
            # print(query)
            search_results = search_results.filter(title=query)
            # print(search_results)

        if filter == "past":
            search_results = search_results.exclude(status="active")
        elif filter == "active":
            search_results = search_results.filter(status="active")

        # Prepare results for frontend
        results = [
            {
                "id": result.id,
                "title": result.title,
                "category": result.category,
                "date": result.date.strftime("%Y-%m-%d"),
                "status": result.status,
                "status_display": result.get_status_display(),
                "price": str(result.price),
                "location": result.location,
                "tickets_sold": str(result.tickets_sold()),
                "revenue": str(result.revenue()),
            }
            for result in search_results
        ]

        return JsonResponse({"results": results}, status=200)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)


@organizer_required
def manage_tickets_view(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    tickets = Ticket.objects.filter(event=event).order_by("-purchased_on")
    page_obj = paginate_queryset(tickets, request, M)
    tickets_json = json.dumps(
        [
            {
                "attender": t.attender.username,
                "event": t.event.title,
                "quantity": t.quantity,
                "purchased_on": t.purchased_on.strftime("%b %d, %Y"),
            }
            for t in page_obj
        ]
    )

    return render(
        request,
        "events/tickets.html",
        {"page_obj": page_obj, "event": event, "tickets_json": tickets_json},
    )


# @login_required
# def sort_tickets_view(request):
#     data = json.loads(request.body)
#     tickets = data.get("tickets")
#     # print(tickets)
#     column = request.GET.get("column")
#     order = request.GET.get("order")

#     if order == "asc":
#         tickets.order_by(column)
#     elif order == "desc":
#         tickets.order_by(-column)
#     print(tickets)

# EventHub
On Eventhub you can explore and buy tickets for events or organize your own.

#### [Watch Video Demo On Youtube](https://youtu.be/u50hHrW1qJc)

![Project Demo](Eventhub-demo.gif)

## Table of Contents
- [Overview](#overview)
- [Distinctiveness and Complexity](#distinctiveness-and-complexity)
- [Features](#features)
- [Project Structure & File Breakdown](#project-structure--file-breakdown)
- [Dependencies](#dependencies)
- [Installation & Usage](#installation-and-usage)
- [Future Improvements](#future-improvements)

---

## Overview

Eventhub is an online platform for organizing and attending real world activities.

### For Attendees
Upon signing up, attendees gain access to an event catalog. They can utilize powerful search and filtering tools by category, location, date, and time to discover activities that match their interests.
The platform allows users to purchase any number of available tickets for an event. The purchasing option is active only for events that have not been completed, cancelled, or sold out.
After they purchase tickets they'll be presented with a confirmation page displaying all details related to their transaction.   
The search and filter features are implemented to enhance user experience by making it faster and easier to discover relevant events.

### For Organizers
Users can create and manage their own events by providing the required details such as event title, description, date and time, location, ticket quantity, and pricing. When a user organizes their first event, they automatically gain access to the Organizer Dashboard. This dashboard allows organizers to view, edit, or cancel their events. It also provides comprehensive ticket sales data, including how many tickets have been sold, how many remain, and overall revenue generated. The dashboard supports filtering, enabling organizers to track and manage all of their events in one place. Access to the dashboard and related management features is restricted to users with organizer status through role-based access control.

## Inspiration

The inspiration for EventHub came from my own experience growing up in Tabriz, Iran, where opportunities for organized entertainment are limited. Despite this, I noticed that many people still create their own activities, such as hosting a picnic with painting, gathering at a café to play a murder mystery board game, or arranging group hiking trips. However, these events typically remain confined to small circles of friends and never reach a wider audience who might also be interested. EventHub was built to address this gap by providing a platform that empowers individuals to share their ideas with a broader community, transforming small, informal gatherings into accessible events for anyone who wishes to participate.


## Distinctiveness and Complexity

### Distinctiveness

EventHub is different from an e-commerce website because while it includes ticketing, that is just one part of a larger platform. It’s specifically distinct from auctions or other transaction-based sites because I had to manage event statuses and ticket quantities dynamically. A large portion of the app focuses on event management tools for organizers, which is not present in prior CS50W projects.

The platform supports both attendees and organizers. Attendees can browse, search, and filter events and purchase tickets, while organizers can create events, manage them, and track sales data through a dashboard. This dual-role functionality and the need to restrict access for non-organizers makes it different from simpler CS50W projects like the Pizza ordering app or basic social networks.

### Complexity

The complexity of EventHub comes from multiple technical challenges implemented across the project:

#### Asynchronous Event Status Updates
Events need to be updated automatically based on date and ticket availability. Using Celery, I created background tasks that update event statuses periodically. Celery beat acts as a heartbeat, checking each event to ensure attendees cannot purchase tickets for past or sold-out events. This requires coordination between the Django app, a message broker, and the Celery worker.

#### Organizer Dashboard
Only accessible to organizers, the dashboard displays all their events, ticket sales, and revenue data. It also supports filtering, searching, and dynamic updates without reloading the page, using JavaScript and API calls. Organizers can edit or cancel events while maintaining accurate ticket and revenue tracking.

#### Role-Based Access
Users start as attendees and automatically become organizers when they create their first event. I implemented a custom decorator that checks user roles before granting access to organizer-specific views, ensuring security and proper functionality across the app.

#### Search and Filter Functionality
The platform allows attendees to filter events by category, location, date, and price range without page reload. This required building robust front-end and back-end interactions using JavaScript and Django views to return filtered JSON results.

#### Ticket Management
Each purchase updates ticket quantities and event statuses in real time. The system handles edge cases like sold-out events, over-purchasing, or expired events, ensuring data integrity across users and events.

## Features

- **Role-Based Access**  
  Restrict certain actions to organizers using custom decorators.

- **Event Management**  
  - Create events with relevant details.  
  - Edit and manage events, including updating status (Active, Canceled, Completed, Sold Out).  
  - Event status updates are automated using Celery for past events.

- **Ticket Management**  
  - Buy tickets for events (only Active events).  
  - Keep track of tickets sold and remaining quantity.  
  - Automatically prevent purchases exceeding availability.

- **Search & Filter Events**  
  - Dynamic search and filtering of events without page reloads using JS and API calls.

- **Organizer Dashboard**  
  - View all events organized by the user.  
  - Filter and search among their events without page reload.  
  - Access detailed sale data, including tickets sold and remaining for each event.



## Project Structure & File Breakdown
```
EventHub/
├── requirements.txt     list of all dependencies
├── README.md            project docs
├── manage.py            used to run commands on the django app
├── db.sqlite3           project's database file
├── celerybeat-schedule  automatically created by celery beat
├── whoosh_index/        automatically created by Whoosh when I built an index
├── media/               the directory used for storing files uploaded by users
│   └── event-images/
├── events/              contains the files for the only app in the project
│   ├── urls.py           contains all the URL patterns for the events app
│   ├── views.py          requests that are made to the app are handled using the view functions
│   ├── models.py         contains all the definitions for my app's Django models 
│   ├── forms.py          the form definition for Event creation based on the Event Model
│   ├── helper.py         includes 2 functions, paginate_queryset & organizer_required decorator  
│   ├── search_indexes.py contains EventIndex definition for haystack (currently unused)
│   ├── tasks.py          contains the definition for celery's scheduled task `update_past_events_status()`
│   ├── utils.py          contains `send_ticket_email()` used for automating sending e-mail notifications
│   ├── admin.py          default file created by django to define which models are displayed on django's admin panel
│   ├── apps.py           default file created by django to configure your app
│   ├── tests.py          automatically created by django which would contain your tests (currently unused)
│   ├── templates/        
│   │   ├── events/       contains all django html templates for the events app
│   │   └── search/       contains event_text.txt, a template used by haystack for indexing
│   └── static/           
│       └── events/       
│           ├── imgs/     used for storing the images I used  such as logo and background images.
│           ├── js/       
│           └── styles/   
└── EventHub/             contains the main project files
    ├── settings.py       contains all configuration settings for the project
    ├── urls.py           contains all the URL patterns for the entire project
    ├── asgi.py           
    ├── wsgi.py           
    ├── __init__.py       
    └── celery.py         sets up and configures celery for the Eventhub project

````


---
### Files  Breakdown 
- **celerybeat-schedule** : it's a sqlite database that celery beat uses to keep track of scheduled tasks. It stores: Which periodic tasks exist, When each task was last run and The next scheduled run time.

- **whoosh-index** : this directory was automatically created by whoosh when i built an index to store search index data.
During the development of this project I experimented with whoosh to allow for  more advanced search capabilities.
Currently I am not using it in the events app but I kept the files for future enhancements.

- **helper.py** : 
- `paginate_queryset()` : a function I wrote similar to the one I used in the Network project
used to paginate any set of objects using django's paginator. 
It's used for displaying a limited number of events on the homepage of the events app and also for displaying a limited number of tickets on the organizer dashboard.

- `organizer_required()` : is a decorator function used for achieving role based access.
this decorator works similarly to django's own `login_required` decorator, It prevents non organizers from accessing features that should be only accessible to organizers.

- `search_indexes.py`: As I mentioned I experimented with haystack whoosh for implementing complex search features, this file includes the core function that would enable that feature. It's only content is a class definition called EventIndex this class is used to index the database table called `events_event` (which was created using the Event model)
Haystack's indexes module lets me define an index for any field in the Event model. Once an index is defined, you can search that field using Haystack. For example, if you only create an index on the title field, then that's the only field you can search through with Haystack.

- `tasks.py` : As mentioned in the [Distinctiveness and Complexity](#distinctiveness-and-complexity)
 section, I used Celery to define tasks that run on a predefined schedule. The tasks.py file is the standard way to integrate Celery with Django. It contains the function that Celery executes on schedule, which is configured in settings.py. 

- `events/templates/events/search/indexes/events/event_text.txt` :
As mentioned before haystack was experimented with, this file is another one of the requirements of enabling haystack's search functionality to work.
this template is used by haystack to figure out what content from the Event model should be indexed for.
currently includes only one line: `{{ object.title }}` which enables haystack to search the title field of the event model.
Although this feature is disabled on the current version of the app I kept the files for future use.

- `Eventhub/celery.py` : 
according to celery's own docs this file is the recommended way to make celery work in your project.
after it loads celery's configuration from the settings.py file, it enables celery to auto discover tasks on its own.


## Dependencies

EventHub requires the following dependencies to run properly:

- **Python 3.12+** – the project is built using Python 3.12.
- **Django 5.1.4** – the main web framework used for building the app.
- **Celery** – for running scheduled tasks in the background.
- **django-celery-beat** – to manage periodic tasks with Celery.
- **Redis** – used as the message broker for Celery (required only if scheduled tasks are enabled).
- **SQLite** – default database for development (`db.sqlite3`).
### Dependencies for Partially Implemented features :  
- **Haystack** – to provide search functionality.
- **Whoosh** – search engine backend for Haystack (currently disabled, kept for future improvements).
- **PayPal SDK** (`paypal.standard.ipn`, `paypal.standard.forms`) – for handling payments.
- **SMTP email setup** – required to send confirmation emails 



## Installation and Usage

1. **Install dependencies**  
   Make sure you have Python 3.12+ installed. Then, in your project directory, run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply migrations**
   Create the database tables required by Django:

   ```bash
   python3 manage.py makemigrations events
   python3 manage.py migrate
   ```

3. **Create a superuser for testing admin features (optional)**

   ```bash
   python3 manage.py createsuperuser
   ```

4. **Run the development server**
   Start the Django server:

   ```bash
   python3 manage.py runserver
   ```

   Eventhub will be available at `http://127.0.0.1:8000/`.

5. **Run Celery for Event Status Update tasks**
   
    Open a new terminal and run:

   ```bash
   celery -A EventHub worker -l info
   celery -A EventHub beat -l info
   ```

   Celery will handle automatically updating event statuses in the background.

6. **Accessing the app**

   * Visit the home page to browse events.
   * Sign Up &  Log in to create events or buy tickets




## Future Improvements

* ### Improve the Organizer Dashboard
  - More detailed Analytics
  - Graphs for statics and analyzing sale data
  
* ### Enhanced Search :
  I experimented with Whoosh for advanced search and filtering. While it’s not needed for the current goals of EventHub, the existing whoosh-index files could be used in the future to implement typo-tolerant or more complex search functionality.
  Implementing this feature will allow users to browse events more efficiently.
* ### Personalized Recommendations:
  * adding a Recommender AI : 
  people who have bought tickets on the website before, get offered events they might be interested in that is similar to what they have enjoyed before.
  * people fill a quiz at sign up which asks them about their interests and suggests events related to those interests.
* ### Automatic E-mail Notifications :
  An E-mail is sent automatically to people who purchase tickets containing their ticket information so that they can use that e-mail on entry to the venue where the event is held. This feature was experimented with but not fully implemented in the current version due to time constraints.
---

## Author : **Negin Jahedi**
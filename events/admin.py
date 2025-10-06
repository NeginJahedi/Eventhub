from django.contrib import admin
from .models import User, Event, Review, Ticket

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Review)
admin.site.register(Ticket)
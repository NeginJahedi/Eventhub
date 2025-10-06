from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create', views.create, name="create"),
    path('Events/<int:event_id>/', views.event_view, name="event"),
    path('Events/<int:event_id>/buyticket', views.buy_ticket_view, name="buy"),
    path('events/search', views.search_view, name="search"),
    path('dashboard/organizer', views.organizer_dashboard, name="organizer"),
    path('dashboard/organizer/edit/<int:event_id>', views.edit_event_view, name="edit_event"),
    path('dashboard/organizer/<int:event_id>/tickets', views.manage_tickets_view, name="tickets"),
    path('dashboard/organizer/filter', views.filter_view, name="filter"),
    # path('tickets/sort', views.sort_tickets_view, name="sort"),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

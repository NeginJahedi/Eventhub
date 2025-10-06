from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from functools import wraps
from django.core.paginator import Paginator


    # function for paginating any queryset:
def paginate_queryset(queryset, request, n):
    paginator = Paginator(queryset, n)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return page_obj



def organizer_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # First ensure the user is logged in
        if not request.user.is_authenticated:
            return redirect('login')

        # Next ensure the user is 'organizer'
        if not request.user.is_organizer:
            raise PermissionDenied("Sorry, This page is only accessible for organizers .")

        return view_func(request, *args, **kwargs)
    return _wrapped_view
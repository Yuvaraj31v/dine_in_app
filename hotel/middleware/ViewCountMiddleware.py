import re

from django.utils.deprecation import MiddlewareMixin
from django.db.models import F
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from hotel.models import Hotel


class FoodViewCountMiddleware(MiddlewareMixin):
    """
    Middleware to track how many times a hotel has been viewed via GET request.

    Increments the 'view_count' of a Hotel when:
    - A valid 'hotel_id' is passed as a query parameter.
    - A valid 'hotel_name' is passed as a query parameter.
    """

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Processes incoming GET requests to '/hotels/' and updates the
        'view_count' field of the matching Hotel.

        Args:
            request: The incoming HTTP request.
            view_func: The view function being called.
            view_args: Positional arguments for the view.
            view_kwargs: Keyword arguments for the view.

        Returns:
            None
        """
        if request.path.startswith('/hotels/') and request.method == 'GET':
            hotel_id = request.GET.get('hotel_id')
            hotel_name = request.GET.get('hotel_name')

            # Increment view_count by hotel_id
            if hotel_id and hotel_id.isdigit():
                try:
                    Hotel.objects.filter(id=int(hotel_id)).update(view_count=F('view_count') + 1)
                except (Hotel.DoesNotExist, ValueError):
                    # Handle invalid hotel_id
                    pass

            # Increment view_count by hotel_name (validated by regex)
            if hotel_name:
                if re.match(r'^[A-Za-z ]{2,100}$', hotel_name):
                    try:
                        Hotel.objects.filter(name=hotel_name).update(view_count=F('view_count') + 1)
                    except ObjectDoesNotExist:
                        # Handle case where hotel with the given name doesn't exist
                        pass
                else:
                    # Optional: Log or handle invalid hotel name format
                    pass

        return None

import logging
from django.core.exceptions import FieldError

from .models import Food
from .serializer import FoodDetailsSerializer, FoodCreateSerializer
from utils.exceptions import BadRequestException

logger = logging.getLogger(__name__)


def get_food_items(request):
    """
    Retrieves food items based on optional query parameters.

    Filters supported:
        - food_id: Get a specific food item by ID
        - hotel_id: Filter foods by hotel ID
        - category_id: Filter foods by category ID

    Raises:
        BadRequestException: For invalid query parameter types or field errors.

    Returns:
        list: Serialized food items.
    """
    try:
        food_id = request.query_params.get('food_id')
        hotel_id = request.query_params.get('hotel_id')
        category_id = request.query_params.get('category_id')

        queryset = Food.objects.select_related('category', 'hotel')

        if food_id:
            food_id = int(food_id)
            queryset = queryset.filter(id=food_id, status__iexact='active')

        if category_id:
            category_id = int(category_id)
            queryset = queryset.filter(category_id=category_id, status__iexact='active')

        if hotel_id:
            hotel_id = int(hotel_id)
            queryset = queryset.filter(hotel_id=hotel_id, status__iexact='active')

        logger.debug("Retrieved %d food item(s).", queryset.count())
        return FoodDetailsSerializer(queryset, many=True).data

    except (ValueError, FieldError) as e:
        logger.warning("Invalid query parameter in get_food_items: %s", str(e))
        raise BadRequestException("Invalid filter value or field.")


def insert_food_items(request):
    """
    Inserts a new food item into the database.

    Expects the following fields in request.data:
        - name: Name of the food
        - price: Positive decimal
        - category: Foreign key (must be active)
        - hotel: Foreign key (must be active)

    Raises:
        BadRequestException: If validation fails.

    Returns:
        dict: Serialized data of the newly created food item.
    """
    serializer = FoodCreateSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()
        logger.info("New food item created: %s (ID: %s)", instance.name, instance.id)
        return serializer.data

    logger.error("Food creation failed due to validation error: %s", serializer.errors)
    raise BadRequestException(str(serializer.errors))

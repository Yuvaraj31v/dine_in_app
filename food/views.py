import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from authenticate.permissions import IsManagerOrAdmin, IsAccessToAll
from .service import get_food_items, insert_food_items
from utils.exceptions import AuthorizationException

logger = logging.getLogger(__name__)


class FoodItemView(APIView):
    """
    Handles GET and POST requests for Food items.
    - GET: Any authenticated user
    - POST: Admin or Manager only
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAccessToAll()]
        elif self.request.method == 'POST':
            return [IsManagerOrAdmin()]
        return super().get_permissions()

    def get(self, request):
        """
        Returns filtered food items based on:
        - food_id
        - hotel_id
        - category_id
        """
        if not request.user or not request.user.is_authenticated:
            logger.warning("Unauthorized GET request to FoodItemView")
            raise AuthorizationException()

        logger.debug("Fetching food items with filters: %s", request.query_params)
        food_items = get_food_items(request)
        logger.info("Food items fetched: %d", len(food_items))
        return Response({'food_items': food_items}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Creates a new food item.
        """
        if not request.user or not request.user.is_authenticated:
            logger.warning("Unauthorized POST request to FoodItemView")
            raise AuthorizationException()

        logger.debug("Creating new food item with data: %s", request.data)
        food_item = insert_food_items(request)
        logger.info("New food item created successfully")
        return Response({'food_items': food_item}, status=status.HTTP_200_OK)

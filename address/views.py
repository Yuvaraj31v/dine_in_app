import logging

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from authenticate.permissions import IsManagerOrAdmin, IsAccessToAll
from .service import insert_address_items, get_address_items, update_address_items
from utils.exceptions import AuthorizationException

logger = logging.getLogger(__name__)


class AddressItemView(APIView):
    """
    API for creating, retrieving, and updating address items.

    Permissions:
        - GET: All roles
        - POST/PATCH: Admin or Manager only
    """

    def get_permissions(self):
        if self.request.method == 'GET':
            return [IsAccessToAll()]
        return [IsManagerOrAdmin()]

    def get(self, request):
        """
        Fetch address item(s). Accessible by all roles.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        logger.debug("GET request received for address items by user: %s", request.user)
        address_items = get_address_items(request)
        return Response({'address_items': address_items}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new address item. Admin/Manager only.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        logger.debug("POST request to create address by user: %s", request.user)
        address_item = insert_address_items(request)
        return Response({'address_item': address_item}, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Update an existing address item. Admin/Manager only.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        logger.debug("PATCH request to update address by user: %s", request.user)
        address_item = update_address_items(request)
        return Response({'address_item': address_item}, status=status.HTTP_200_OK)
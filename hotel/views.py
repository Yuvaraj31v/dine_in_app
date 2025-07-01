from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from authenticate.permissions import IsManagerOrAdmin, IsAccessToAll
from .service import get_hotel_item, insert_hotel_items, update_hotel_item, remove_hotel
from utils.exceptions import AuthorizationException


class HotelItemView(APIView):
    """
    Handles operations related to Hotel items.

    Permissions:
        - GET: All authenticated users
        - POST, PATCH, DELETE: Admin and Manager only
    """

    def get_permissions(self):
        """
        Return appropriate permission classes
        based on the request method.
        """
        if self.request.method == 'GET':
            return [IsAccessToAll()]
        elif self.request.method in ['POST', 'PATCH', 'DELETE']:
            return [IsManagerOrAdmin()]
        return super().get_permissions()

    def get(self, request):
        """
        Handle GET request to fetch hotel data.

        Filters:
            - hotel_id
            - hotel_name
            - area

        Returns:
            Filtered hotel list in response.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        data = get_hotel_item(request)
        return Response({'hotel_item': data}, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handle POST request to create a hotel.

        Requires:
            - Valid hotel data
            - Admin or Manager access

        Returns:
            Created hotel info.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        hotel_item = insert_hotel_items(request)
        return Response({'hotel_items': hotel_item}, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Handle PATCH request to update a hotel.

        Fields:
            - name (optional)
            - address_id (optional)

        Returns:
            Updated hotel data.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        hotel_item = update_hotel_item(request)
        return Response({'hotel_item': hotel_item}, status=status.HTTP_200_OK)

    def delete(self, request):
        """
        Handle DELETE request to deactivate a hotel.

        Requires:
            - hotel_id in query params

        Returns:
            Success message upon deactivation.
        """
        remove_hotel(request)
        return Response({"message": "Hotel deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

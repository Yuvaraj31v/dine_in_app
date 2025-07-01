from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from authenticate.permissions import IsManagerOrAdmin, IsAccessToAll
from orders.service import insert_cart_details, update_cart_item
from utils.exceptions import AuthorizationException


class CartItemView(APIView):
    """
    Handles cart item creation and updates.

    Permissions:
        - GET: All authenticated users
        - POST, PATCH: Admin/Manager only
    """

    def get_permissions(self):
        """
        Returns permission class based on method.
        """
        if self.request.method == 'GET':
            return [IsAccessToAll()]
        elif self.request.method in ['POST', 'PATCH']:
            return [IsManagerOrAdmin()]
        return super().get_permissions()

    def post(self, request):
        """
        Creates cart and adds item.

        Payload:
            - food (int)
            - quantity (int)

        Returns:
            JSON response with added cart item.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        cart_detail_data = {
            'user': request.user.id,
            'total_price': 0
        }

        cart_item = insert_cart_details(request, cart_detail_data)
        return Response({'cart_item': cart_item}, status=status.HTTP_200_OK)

    def patch(self, request):
        """
        Updates cart item quantity.

        Payload:
            - id (int)
            - quantity (int)

        Returns:
            JSON response with updated cart item.
        """
        if not request.user or not request.user.is_authenticated:
            raise AuthorizationException()

        updated_cart_item = update_cart_item(request)
        return Response({'cart_item': updated_cart_item}, status=status.HTTP_200_OK)

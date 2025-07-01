import logging

from .serializer import (
    CartDetailCreateSerializer,
    CartItemCreateSerializer,
    CartItemUpdateSerializer
)
from .models import CartDetails, CartItem
from utils.exceptions import BadRequestException

logger = logging.getLogger(__name__)


def insert_cart_details(request, cart_detail_data):
    """
    Creates/uses a cart and adds item to it.

    Request must include:
        - food (int)
        - quantity (int)

    Returns:
        dict: Created CartItem data.
    """
    user = cart_detail_data.get('user')
    existing_cart = CartDetails.objects.filter(user=user).first()

    if not existing_cart:
        logger.debug("No cart found for user. Creating new cart.")
        serializer = CartDetailCreateSerializer(data=cart_detail_data)
        if serializer.is_valid():
            cart_instance = serializer.save()
            cart_id = cart_instance.id
            logger.info("Cart created for user %s", user)
        else:
            logger.error("Cart creation failed: %s", serializer.errors)
            raise BadRequestException(serializer.errors)
    else:
        logger.debug("Using existing cart for user %s", user)
        cart_id = existing_cart.id

    cart_item_data = request.data.copy()
    cart_item_data['cart'] = cart_id

    item_serializer = CartItemCreateSerializer(data=cart_item_data)
    if item_serializer.is_valid():
        item_serializer.save()
        logger.info("Cart item added to cart %s", cart_id)
        return item_serializer.data

    logger.error("Cart item creation failed: %s", item_serializer.errors)
    raise BadRequestException(item_serializer.errors)


def update_cart_item(request):
    """
    Updates quantity of existing cart item.

    Request must include:
        - id: CartItem ID
        - quantity: New value

    Returns:
        dict: Updated CartItem data.
    """
    item_id = request.data.get('id')
    new_qty = request.data.get('quantity')

    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.quantity = new_qty

        serializer = CartItemUpdateSerializer(cart_item)
        if serializer.is_valid():
            serializer.save()
            logger.info("Updated cart item %s with quantity %s", item_id, new_qty)
            return serializer.data
        logger.error("Cart item update invalid: %s", serializer.errors)
    except CartItem.DoesNotExist:
        logger.warning("Cart item not found: %s", item_id)
        raise BadRequestException({'id': 'Cart item does not exist'})

from rest_framework import serializers

from .models import CartDetails, CartItem
from utils.exceptions import BadRequestException


class CartItemCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create a new CartItem.
    Includes custom validation for food status, quantity, and cart status.
    """

    class Meta:
        model = CartItem
        fields = ['food', 'quantity', 'cart']

    def validate_food(self, value):
        """
        Validates that the selected food is still active.
        """
        if value.status != "Active":
            raise BadRequestException(f"The food item '{value}' is no longer available.")
        return value

    def validate_quantity(self, value):
        """
        Ensures that the quantity is not zero.
        """
        if value == 0:
            raise BadRequestException("Quantity must be at least 1.")
        return value

    def validate_cart(self, value):
        """
        Ensures the associated cart is active.
        """
        if value.status != "Active":
            raise BadRequestException("The selected cart is not active.")
        return value


class CartDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer to create CartDetails for a user.
    """

    class Meta:
        model = CartDetails
        fields = ['user', 'total_price']


class CartItemUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer to update CartItem quantity or food reference.
    """

    class Meta:
        model = CartItem
        fields = ['id', 'food', 'quantity']

    def validate_food(self, value):
        """
        Validates that the selected food is still active.
        """
        if value.status != "Active":
            raise BadRequestException(f"The food item '{value}' is no longer available.")
        return value

    def validate_quantity(self, value):
        """
        Ensures that the quantity is not zero.
        """
        if value == 0:
            raise BadRequestException("Quantity must be at least 1.")
        return value
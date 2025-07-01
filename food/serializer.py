import re
from rest_framework import serializers

from .models import Food, Category
from hotel.models import Hotel
from utils.exceptions import BadRequestException


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = ['id', 'name']


class HotelSerializer(serializers.ModelSerializer):
    """
    Serializer for Hotel model.
    """

    class Meta:
        model = Hotel
        fields = ['id', 'name']


class FoodDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Food details with nested Category and Hotel info.
    """

    category = CategorySerializer(read_only=True)
    hotel = HotelSerializer(read_only=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'hotel', 'category']


class FoodCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Food item with validation.
    """

    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Food
        fields = ['name', 'price', 'category', 'hotel']

    def validate_name(self, value):
        """
        Validates food name: only alphabets and spaces allowed (2–100 chars).
        """
        if not re.match(r'^[A-Za-z ]{2,100}$', value):
            raise BadRequestException("Given name is invalid.")
        return value

    def validate_price(self, value):
        """
        Validates that price is a positive decimal (max 2 decimal places).
        """
        value_str = str(value)
        if not re.match(r'^\d+(\.\d{1,2})?$', value_str) or value <= 0:
            raise BadRequestException("Given price is invalid.")
        return round(value, 2)

    def validate_category(self, value):
        """
        Ensures category is active.
        """
        if value.status != "Active":
            raise BadRequestException("Given category is inactive.")
        return value

    def validate_hotel(self, value):
        """
        Ensures hotel is active.
        """
        if value.status != "Active":
            raise BadRequestException("Given hotel is inactive.")
        return value

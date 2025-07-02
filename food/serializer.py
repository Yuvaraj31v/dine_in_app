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

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['price_with_tax'] = f"₹{round(float(rep['price']), 2)}"
        rep['price'] = f"₹{rep['price']}"
        rep['currency'] = "INR"
        return rep


class FoodCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a Food item with validation.
    """

    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'category', 'hotel']

    def validate_name(self, value):
        """
        Validates food name: only alphabets and spaces allowed (2–100 chars).
        """
        if not re.match(r'^[A-Za-z ]{2,100}$', value):
            raise BadRequestException(key="INVALID_FOOD_NAME")
        return value

    def validate_price(self, value):
        """
        Validates that price is a positive decimal (max 2 decimal places).
        """
        value_str = str(value)
        if not re.match(r'^\d+(\.\d{1,2})?$', value_str) or value <= 0:
            raise BadRequestException(key='INVALID_PRICE')
        return round(value, 2)

    def validate_category(self, value):
        """
        Ensures category is active.
        """
        if value.status != "Active":
            raise BadRequestException(key="INACTIVE_CATEGORY")
        return value

    def validate_hotel(self, value):
        """
        Ensures hotel is active.
        """
        if value.status != "Active":
            raise BadRequestException(key='INACTIVE_HOTEL')
        return value


class FoodOnlyViewSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Food details only.
    """

    class Meta:
        model = Food
        fields = ['id', 'name', 'price']

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['price_with_tax'] = f"₹{round(float(rep['price']), 2)}"
        rep['price'] = f"₹{rep['price']}"
        rep['currency'] = "INR"
        return rep
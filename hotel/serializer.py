import re

from rest_framework import serializers

from .models import Hotel
from address.models import Address
from utils.exceptions import BadRequestException
from food.serializer import  FoodOnlyViewSerializer

class AddressSerializer(serializers.ModelSerializer):
    """
    Serializer for Hotel model with nested adress serializers.
    Returns:
        area: String - Area of the Hotel located.
        street: String - Street of the Hotel located.
        city: String - City of the Hotel located.
    """

    class Meta:
        model = Address
        fields = ['area','street','city']


class HotelItemViewSerializer(serializers.ModelSerializer):
    """
    Serializer for Hotel model with nested adress serializers.
    Returns:
        id: Integer - Primary key of the Hotel item.
        name: String - Name of the Hotel.
        adress: Object - Nested adress serializer.
        created_at, updated_at, status: Metadata fields.
    """

    address = AddressSerializer(read_only=True)
    food_items = serializers.SerializerMethodField()
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address','status', 'food_items']

    def get_food_items(self, obj):
        active_foods = obj.foods.filter(status__iexact='active')
        return FoodOnlyViewSerializer(active_foods, many=True).data
    
    def to_representation(self, instance):
        """
        Increment view count before serializing
        """
        instance.increment_view_count()
        return super().to_representation(instance)


class HotelCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Hotel objects with validation.
    Validations:
        - Name must be alphabetic with spaces only.
        - Address must have an 'Active' status.
    """

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'address', 'user']
        extra_kwargs = {
            'address': {'validators': []},
            'user': {'validators': []}
        }

    def validate_name(self, value):
        """
        Validates the 'name' field of the food item.
        Returns:
            str: Validated name.
        """
        pattern = r'^[A-Za-z ]{2,100}$'
        if not re.match(pattern, value):
            raise BadRequestException(key='INVALID_HOTEL_NAME')
        return value

    def validate_address(self, value):
        """
        Validates the 'address' foreign key field.
        Returns:
            Address: Validated address object.
        """
        if value.status != "Active":
            raise BadRequestException(key='INACTIVE_ADDRESS')
        if Hotel.objects.filter(address=value).exists():
                raise BadRequestException(key='HOTEL_WITH_ADDRESS_EXISTS')
        return value

    
class HotelUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Hotel objects with validation.
    Returns:
        Hotel: Validated hotel object
    """
    class Meta:
        model = Hotel
        fields = ['name','address']

    def validate_address(self, value):
        """
        Validates the 'address' foreign key field.
        Returns:
            Address: Validated address object.
        """
        if value.status != "Active":
            raise BadRequestException(key='INACTIVE_ADDRESS')
        return value
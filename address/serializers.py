import logging

from rest_framework import serializers

from .models import Address
from utils.postal_api import get_city_state_from_pincode
from utils.exceptions import BadRequestException

logger = logging.getLogger(__name__)  # Logger for this serializer module

class AddressCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating Address records.
    Includes validation for street, area, and pincode.
    """

    class Meta:
        model = Address
        fields = ['id', 'area', 'street', 'pincode']

    def validate_street(self, value):
        """
        Validates the 'street' field: cannot be empty or too short.
        """
        if not value.strip():
            logger.debug("Street validation failed: empty string")
            raise BadRequestException("Street cannot be empty.")
        if len(value) < 3:
            logger.debug("Street validation failed: less than 3 characters")
            raise BadRequestException("Street must be at least 3 characters long.")
        return value

    def validate_area(self, value):
        """
        Validates the 'area' field: cannot be empty or too short.
        """
        if not value.strip():
            logger.debug("Area validation failed: empty string")
            raise BadRequestException("Area cannot be empty.")
        if len(value) < 3:
            logger.debug("Area validation failed: less than 3 characters")
            raise BadRequestException("Area must be at least 3 characters long.")
        return value

    def validate_pincode(self, value):
        """
        Validates the 'pincode' field: must be a 6-digit number
        and must return valid city/state from postal API.
        """
        if not str(value).isdigit() or len(str(value)) != 6:
            logger.debug(f"Pincode validation failed: not a 6-digit number -> {value}")
            raise BadRequestException("Pincode must be a 6-digit number.")

        logger.debug(f"Fetching city/state for pincode: {value}")
        location = get_city_state_from_pincode(value)
        logger.debug(f"Location fetched from pincode {value}: {location}")

        if not location.get('city') or not location.get('state'):
            logger.debug(f"Invalid or unsupported pincode: {value}")
            raise BadRequestException("Invalid or unsupported pincode.")

        return value


class AddressViewItemSerializer(serializers.ModelSerializer):
    """
    Serializer for viewing Address records.
    Includes all readable address fields.
    """

    class Meta:
        model = Address
        fields = ['id', 'area', 'street', 'city', 'state', 'pincode']
import logging
import re

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from .serializers import AddressCreateSerializer, AddressViewItemSerializer
from .models import Address
from utils.exceptions import BadRequestException

logger = logging.getLogger(__name__)  # Logger for debugging

def insert_address_items(request):
    """
    Inserts a new address item into the database.

    Expects the following fields in request.data:
        - area: Area of the address
        - street: Street name
        - pincode: 6-digit pincode

    Raises:
        BadRequestException: If validation fails.

    Returns:
        dict: Serialized data of the newly created address item.
    """
    logger.debug("Starting insert_address_items with data: %s", request.data)
    serializer = AddressCreateSerializer(data=request.data)

    if serializer.is_valid():
        address = serializer.save()
        logger.info("Address created successfully with ID: %s", address.id)
        return serializer.data

    logger.error("Address creation failed due to validation error: %s", serializer.errors)
    raise BadRequestException(str(serializer.errors))


def get_address_items(request):
    """
    Retrieves one or more active address items.

    Query params (optional):
        - address_id: ID of the address to retrieve

    Returns:
        list: Serialized address data.
    """
    address_id = request.query_params.get('address_id')
    logger.debug("Fetching address with ID: %s", address_id)

    if address_id:
        address_items = Address.objects.filter(id=address_id, status='Active')
    else:
        address_items = Address.objects.filter(status='Active')

    serializer = AddressViewItemSerializer(address_items, many=True)
    logger.info("Fetched %d address item(s)", len(serializer.data))
    return serializer.data


def update_address_items(request):
    """
    Updates area and/or street for an existing address item.

    Expects the following fields in request.data:
        - address_id (required)
        - area (optional)
        - street (optional)

    Returns:
        dict: Serialized updated address item.

    Raises:
        BadRequestException: If validation or update fails.
    """
    address_id = request.data.get('address_id')
    area = request.data.get('area')
    street = request.data.get('street')

    logger.debug("Updating address with ID: %s", address_id)

    if not address_id:
        logger.warning("Missing address_id in update request")
        raise BadRequestException("Address ID is required to update address.")

    update_data = {}

    if area:
        if not re.match(r'^[A-Za-z ]{2,100}$', area):
            logger.debug("Area validation failed: %s", area)
            raise BadRequestException("Invalid address format or field.")
        update_data['area'] = area

    if street:
        if not re.match(r'^[A-Za-z ]{2,100}$', street):
            logger.debug("Street validation failed: %s", street)
            raise BadRequestException("Invalid address format or field.")
        update_data['street'] = street

    try:
        Address.objects.filter(id=address_id).update(**update_data)
        address_item = Address.objects.get(id=address_id, status="Active")
        logger.info("Address with ID %s updated successfully", address_id)
    except ObjectDoesNotExist:
        logger.error("Address with ID %s not found", address_id)
        raise BadRequestException("Address ID not present")
    except IntegrityError:
        logger.error("Integrity error while updating address ID: %s", address_id)
        raise BadRequestException("Given address not present")

    return AddressViewItemSerializer(address_item).data

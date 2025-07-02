import re
import logging

from django.db import IntegrityError
from django.core.exceptions import FieldError, ObjectDoesNotExist

from .models import Hotel
from address.models import Address
from .serializer import (
    HotelItemViewSerializer,
    HotelCreateSerializer,
    HotelUpdateSerializer,
)
from utils.exceptions import BadRequestException

logger = logging.getLogger(__name__)

VALID_NAME_PATTERN = r'^[A-Za-z ]{2,100}$'


def get_hotel_item(request):
    """
    Returns hotel(s) filtered by ID, name, or area.
    """

    hotel_id = request.query_params.get('hotel_id')
    hotel_name = request.query_params.get('hotel_name')
    area = request.query_params.get('area')

    try:
        if hotel_id:
            hotel_id = int(hotel_id)
            logger.debug("Filter: hotel_id = %s", hotel_id)
            queryset = Hotel.objects.filter(id=hotel_id, status='Active')

        elif hotel_name:
            if not re.fullmatch(VALID_NAME_PATTERN, hotel_name):
                raise BadRequestException(key='INVALID_HOTEL_NAME')
            logger.debug("Filter: hotel_name = %s", hotel_name)
            queryset = Hotel.objects.filter(name=hotel_name, status='Active')

        elif area:
            if not re.fullmatch(VALID_NAME_PATTERN, area):
                raise BadRequestException(key="INVALID_AREA")
            logger.debug("Filter: area = %s", area)
            queryset = Hotel.objects.filter(address__area=area, status='Active')

        else:
            logger.debug("No filters applied. Fetching all active hotels.")
            queryset = Hotel.objects.filter(status='Active')

        logger.info("Hotels retrieved: %s", queryset.count())
        return HotelItemViewSerializer(queryset, many=True).data

    except (ValueError, FieldError) as e:
        logger.error("Filter error in get_hotel_item: %s", str(e))
        raise BadRequestException(key='INVALID_HOTEL_FIELD_OR_FORMAT')


def insert_hotel_items(request):
    """
    Creates a new hotel item.
    """

    logger.debug("Insert hotel request data: %s", request.data)
    serializer = HotelCreateSerializer(data=request.data)

    if serializer.is_valid():
        try:
            serializer.save()
            return serializer.data
        except IntegrityError as e:
            logger.error("Insert failed due to integrity error: %s", str(e))
            raise BadRequestException(key='HOTEL_WITH_ADDRESS_EXISTS')
    raise BadRequestException(str(serializer.errors))

def update_hotel_item(request):
    """
    Updates hotel name and/or address.
    """

    hotel_id = request.data.get('id')
    hotel_name = request.data.get('name')
    address_id = request.data.get('address_id')

    if not hotel_id:
        raise BadRequestException(key='HOTEL_ID_REQUIRED')

    update_data = {}

    if hotel_name:
        if not re.fullmatch(VALID_NAME_PATTERN, hotel_name):
            raise BadRequestException(key='INVALID_HOTEL_NAME')
        update_data['name'] = hotel_name

    if address_id:
        try:
            address_id = int(address_id)
            if not Address.objects.filter(id=address_id, status='Active').exists():
                raise BadRequestException("Inactive or missing address.")
            update_data['address_id'] = address_id
        except (ValueError, FieldError) as e:
            logger.error("Invalid address ID: %s", str(e))
            raise BadRequestException("Invalid address ID.")

    try:
        queryset = Hotel.objects.filter(id=hotel_id)
        if not queryset.exists():
            raise BadRequestException(key='NO_HOTEL_FOUND')
        queryset.update(**update_data)
        hotel = queryset.first() 
        logger.info("Hotel updated: %s", hotel_id)
        return HotelUpdateSerializer(hotel).data
    except IntegrityError as e:
        logger.error("Integrity error during update: %s", str(e))
        raise BadRequestException("Invalid update due to duplicate constraints.")


def remove_hotel(request):
    """
    Marks hotel as inactive.
    """

    hotel_id = request.query_params.get('hotel_id')

    if not hotel_id:
        raise BadRequestException(key='HOTEL_ID_REQUIRED')

    try:
        hotel_id = int(hotel_id)
        hotel = Hotel.objects.get(id=hotel_id)
        hotel.status = "inactive"
        hotel.save()
        logger.info("Hotel deactivated: %s", hotel_id)
        return {"message": f"Hotel {hotel_id} deactivated."}
    except (ValueError, FieldError) as e:
        logger.error("Invalid hotel_id format: %s", str(e))
        raise BadRequestException(key='INVALID_HOTEL_FIELD_OR_FORMAT')
    except ObjectDoesNotExist:
        raise BadRequestException(key="NO_HOTEL_FOUND")

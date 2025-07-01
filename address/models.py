from django.db import models
from utils.models import BaseModel
from utils.postal_api import get_city_state_from_pincode


class Address(BaseModel):
    """
    Represents a physical address for a hotel or user.
    Automatically fetches city and state from the given pincode.
    """

    area = models.CharField(max_length=100, null=False)  # Local area name
    street = models.CharField(max_length=100, null=False)  # Street name
    city = models.CharField(max_length=100, blank=True, null=False)  # Auto-filled from pincode
    state = models.CharField(max_length=100, blank=True, null=False)  # Auto-filled from pincode
    pincode = models.PositiveBigIntegerField(null=False)  # 6-digit postal code

    def save(self, *args, **kwargs):
        """
        Overrides default save to fetch city and state from pincode
        before saving the model instance.
        """
        if self.pincode:
            data = get_city_state_from_pincode(self.pincode)
            self.city = data['city']
            self.state = data['state']
        super().save(*args, **kwargs)

    def __str__(self):
        """
        String representation of the address instance.
        """
        return f"{self.street} {self.area} {self.city} {self.state} {self.pincode}"

from django.db import models

from utils.models import BaseModel
from address.models import Address
from authenticate.models import CustomUser


class Hotel(BaseModel):
    """
    Represents a hotel/restaurant that lists food items.
    Each hotel is associated with a unique user (Hotel Manager) and an address.
    """

    name = models.CharField(
        max_length=100,
        null=False,
        help_text="Name of the hotel."
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        null=False,
        help_text="Hotel manager (one user per hotel)."
    )
    address = models.OneToOneField(
        Address,
        on_delete=models.CASCADE,
        null=False,
        help_text="Address of the hotel (one address per hotel)."
    )
    view_count = models.PositiveIntegerField(
        default=0,
        null=False,
        help_text="Number of times the hotel page was viewed."
    )

    def __str__(self):
        """Returns a readable string representation of the hotel."""
        return self.name
    
    def increment_view_count(self):
        """
        Increments the view count of the hotel.
        Useful for tracking hotel popularity.
        """
        self.view_count += 1
        self.save(update_fields=['view_count'])


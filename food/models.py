from django.db import models
from utils.models import BaseModel
from hotel.models import Hotel


class Category(BaseModel):
    """
    Represents a food category (e.g., Biriyani, Desserts, Drinks).
    """

    name = models.CharField(max_length=100, null=False)  # Category name

    def __str__(self):
        """
        String representation of the category.
        """
        return self.name


class Food(BaseModel):
    """
    Represents an individual food item listed by a hotel.
    Each food is linked to a category and a hotel.
    """

    name = models.CharField(max_length=100, null=False)  # Name of the food item
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)  # Price in ₹
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=False)  # Linked category
    hotel = models.ForeignKey(
        Hotel,
        on_delete=models.CASCADE,
        related_name='foods',
        null=False
    )  # Hotel that offers this food item

    def __str__(self):
        """
        String representation of the food item.
        """
        return f"{self.name} - ₹{self.price}"

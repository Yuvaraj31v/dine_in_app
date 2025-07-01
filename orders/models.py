from decimal import Decimal

from django.db import models
from django.db.models import Sum, F

from utils.models import BaseModel
from authenticate.models import CustomUser
from food.models import Food


class CartDetails(BaseModel):
    """
    Represents a user's cart summary.

    Fields:
        - total_price: Total price of all items in the cart
        - user: One-to-one relationship with a user

    Notes:
        - Each user can have only one active cart
    """
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    def update_total_price(self):
        """
        Updates total_price based on current cart items.

        Calculates:
            Sum of (price * quantity) for all items
        """
        total = self.cartitem_set.aggregate(
            total=Sum(F('price') * F('quantity'))
        )['total'] or Decimal('0.00')

        self.total_price = total
        self.save(update_fields=['total_price'])


class CartItem(BaseModel):
    """
    Represents an item in a user's cart.

    Fields:
        - price: Price at the time item was added
        - quantity: Number of units
        - food: Reference to the food item
        - cart: Foreign key to the user's cart

    Notes:
        - Price is preserved even if the food item's price changes later
    """
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    quantity = models.PositiveSmallIntegerField(null=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=False)
    cart = models.ForeignKey(CartDetails, on_delete=models.CASCADE, null=False)

    def save(self, *args, **kwargs):
        """
        Saves the item and updates the total cart price.

        Behavior:
            - Sets price from food if not provided
            - Updates CartDetails.total_price after saving
        """
        if not self.price:
            self.price = self.food.price

        super().save(*args, **kwargs)
        self.cart.update_total_price()
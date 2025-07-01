from django.db.models.signals import post_save
from django.dispatch import receiver
from hotel.models import Hotel
from food.models import Food

@receiver(post_save, sender=Hotel)
def deactivate_foods_if_hotel_inactive(sender, instance, **kwargs):
    """
    Signal to deactivate all foods under a hotel if hotel is inactive.
    """
    if instance.status == 'inactive':
        Food.objects.filter(hotel=instance).update(status='inactive')
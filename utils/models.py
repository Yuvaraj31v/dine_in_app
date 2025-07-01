from django.db import models


class BaseModel(models.Model):
    STATUS_CHOICES = (
        ('ACTIVE',),
        ('INACTIVE',),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(
        choices=[('active', 'Active'), ('inactive', 'Inactive')],
        max_length=20,
        default="Active"
    )


    class Meta:
        abstract = True 
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import TextChoices


class UserTypeChoices(TextChoices):
    CUSTOMER = "customer"
    AGENT = "agent"


class User(AbstractUser):
    user_type = models.SlugField(choices=UserTypeChoices.choices, null=True, default=UserTypeChoices.CUSTOMER.value)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

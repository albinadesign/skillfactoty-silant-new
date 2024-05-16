from django.db import models

from django.contrib.auth.models import AbstractUser, User

class User(AbstractUser):
    is_client = models.BooleanField(default=False)
    is_service_company = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    last_name = models.CharField('Полное название компании', max_length=150, blank=True)

    def __str__(self):
        return self.last_name if self.is_client or self.is_service_company else self.username
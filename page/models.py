from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('branch_admin', 'Branch Admin'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=12, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.username} - {self.role} - id-{self.id}"

    















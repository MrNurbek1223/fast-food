from django.db import models
from page.models import User
from django.contrib.gis.db import models

class Branch(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='branches/')
    description = models.TextField()
    location = models.PointField()
    address = models.CharField(max_length=255)
    admin = models.ForeignKey(User, on_delete=models.CASCADE, related_name='admin_branches', limit_choices_to={'role': 'branch_admin'})  # Filial admini

    def __str__(self):
        return f"{self.name} - {self.id}"
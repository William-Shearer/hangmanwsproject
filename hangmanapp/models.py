from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    def __str__(self):
        return f"User {self.id}: {self.first_name} {self.last_name} ({self.username}) created {self.date_joined.strftime('%Y %m %d')}"

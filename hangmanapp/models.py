from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

    def __str__(self):
        return f"User {self.id}: {self.first_name} {self.last_name} ({self.username}) created {self.date_joined.strftime('%Y %m %d')}"


class UserWordHistory(models.Model):
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    word = models.CharField(max_length = 60, blank = True, null = True)
    player_word = models.CharField(max_length = 60, blank = True, null = True)
    hits = models.PositiveIntegerField(default = 0)
    misses = models.PositiveIntegerField(default = 0)
    used_letters = models.CharField(max_length = 30, blank = True, null = True)
    complete = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.word} for user {self.user.username} completed {self.completed}"
 
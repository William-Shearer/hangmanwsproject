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
    won = models.BooleanField(default = False)

    """
    Superceded. This was the initial idea, but I have decided that there is
    nothing wrong with repeating words, only not too frequently.
    An implementation of the improved mechanism is in functions.py.
    class Meta:
        unique_together = ["user", "word"]
    """

    def __str__(self):
        return f"The word \"{self.word.upper()}\" for user {self.user.username}, completed {self.complete}"
    

class UserScoreCard(models.Model):
    """
    There are one of these ScoreCards for each user.
    How the scoring system works.
    Primarily, the ratio of the words won to total words, per user, is used.
    won_words / total_words gives the percentage score of this ratio.
    A secondary score is figured as an efficiency rating of won words.
    win_efficiency = total_hits_in_won_words / (total_hits_in_won_words + total_misses_in_won_words)
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    win_ratio = models.PositiveSmallIntegerField(default = 0)
    win_efficiency = models.PositiveSmallIntegerField(default = 0)
    word_count = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"ScoreCard for {self.user.username} with {self.word_count} words"
    

class GuestBook(models.Model):
    """
    Only one signature per user is permitted, so the use of OnToOneField is ideal 
    to control that by default.
    """
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    comment = models.TextField()
    created = models.DateTimeField(auto_now = False, auto_now_add = True)

    def __str__(self):
        return f"Guestbook entry for {self.user.username} on {self.created.strftime('%Y %m %d')}"
    

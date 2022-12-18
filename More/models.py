from django.db import models
from Account.models import User

class ImprovementSuggestions(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    suggestion = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username

class FeedBack(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    feedback = models.TextField()
    date = models.DateTimeField()

    def __str__(self):
        return self.user.username

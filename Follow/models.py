from django.db import models
from Account.models import User

class Friend(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="user")
    followers = models.ManyToManyField(User,related_name="followers",blank=True)
    following = models.ManyToManyField(User,related_name="following",blank=True)
    mutual = models.ManyToManyField(User,related_name="mutual",blank=True)
    

    def __str__(self):
        return self.user.username

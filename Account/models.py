from django.db import models
from django.contrib.auth.models import AbstractUser
from PIL import Image

class User(AbstractUser):
    profile_image = models.ImageField(upload_to="profile",null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    skill = models.CharField(max_length=100,null=True,blank=True)
    name = models.CharField(max_length=100,null=True,blank=True)
    active_status = models.BooleanField(default=False)

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if self.profile_image:
            img = Image.open(self.profile_image.path)
            if img.width >= 600 or img.height >= 600:
                output_size = (600,600)
                img.thumbnail(output_size,Image.LANCZOS)
                img.save(self.profile_image.path)
            else:
                output_size = (img.width,img.height)
                img.thumbnail(output_size,Image.LANCZOS)
                img.save(self.profile_image.path)
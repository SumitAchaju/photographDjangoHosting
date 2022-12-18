from django.db import models
from Account.models import User
from PIL import Image

class PostImage(models.Model):
    image = models.ImageField(upload_to="PostImages")

    def save(self,*args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            img = Image.open(self.image.path)
            if img.width >= 900 or img.height >= 900:
                output_size = (900,900)
                img.thumbnail(output_size,Image.LANCZOS)
                img.save(self.image.path)
            else:
                output_size = (img.width,img.height)
                img.thumbnail(output_size,Image.LANCZOS)
                img.save(self.image.path)

    def __str__(self):
        return self.image.name

class Comment(models.Model):
    comment_by = models.ForeignKey(User,on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment_by.username

class Category(models.Model):
    image = models.ImageField(upload_to="CategoryImage")
    discription = models.CharField(max_length=50)
    title = models.CharField(max_length=40,unique=True)

    def __str__(self):
        return self.title

class Post(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="post_user")
    caption = models.TextField(null=True,blank=True)
    postimage = models.ManyToManyField(PostImage)
    like_by = models.ManyToManyField(User,related_name="like_users",blank=True)
    comment = models.ManyToManyField(Comment,related_name="comments",blank=True)
    post_date = models.DateTimeField(null=True,blank=True)
    category = models.ManyToManyField(Category)
    saved_by = models.ManyToManyField(User,blank=True)

    def __str__(self):
        return self.user.username

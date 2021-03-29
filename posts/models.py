from django.db import models
from users.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=250)
    alias = models.CharField(max_length=50)


class Post(models.Model):
    title = models.TextField(max_length=250, blank=False)
    description = models.TextField(max_length=150)
    text = models.TextField(max_length=1000, blank=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='img/', blank=True)
    video = models.URLField(blank=True)
    created_date = models.DateTimeField(
        default=timezone.now)





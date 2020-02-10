from django.db import models
from django.contrib.auth.models import User
from PIL import Image


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    phone = models.IntegerField()
    description = models.TextField(max_length=500)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 590 or img.width > 590:
            output_size = (590, 590)
            img.thumbnail(output_size)
            img.save(self.image.path)

from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone


from PIL import Image
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default="default.png",
                              upload_to='profile_pics', null=True)
    bio = models.CharField(
        default=" It provides a way to assign permissions to specific users and groups of users.", max_length=200, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return f'{self.user.username} profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

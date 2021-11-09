from django.db import models
from django.contrib.auth.models import User

from django.utils import timezone

from django.urls import reverse

from django.shortcuts import redirect

from ckeditor.fields import RichTextField

from django.utils.text import slugify 
# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    content = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default=timezone.now, null=True)
    slug = models.SlugField()
    views = models.IntegerField(default=0, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args,**kwargs) :
        self.slug = slugify(self.title)
        return super().save(*args,**kwargs)

    class Meta:
        ordering = ['-id']

    # def get_absolute_url(self):
    #     return reverse("post-detail", kwargs={"pk": self.pk})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=200, null=True)
    time = models.DateTimeField(default=timezone.now, null=True)
    parent = models.ForeignKey(
        'self', related_name="rahul", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.comment[:25] }    by  - {self.user}'

from django.db import models
from django.utils import timezone
from main.managers import PublishedManager
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    name         = models.CharField(max_length = 100)

    def __str__(self):
        return self.name


class News(models.Model):

    class Status(models.TextChoices):
        Draft     = "DF", "Draft"
        Published = "Pb", "Published"
    title         = models.CharField(max_length = 255)
    slug          = models.SlugField(max_length = 255)
    body          = models.TextField()
    user          = models.ForeignKey(User, on_delete=models.CASCADE)
    image         = models.ImageField(upload_to = 'news/images')
    category      = models.ForeignKey('Category', on_delete = models.CASCADE)
    publish_time  = models.DateTimeField(default = timezone.now)
    create_time   = models.DateTimeField(auto_now_add = True)
    update_time   = models.DateTimeField(auto_now = True)
    status        = models.CharField(max_length = 2,
                                    choices = Status.choices,
                                    default = Status.Draft)
    objects       = models.Manager()
    published     = PublishedManager()

    class Meta:
        ordering = ['-publish_time']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('single', args=[self.slug])

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Contact(models.Model):
    name    = models.CharField(max_length=150)
    email   = models.EmailField(max_length=150)
    message = models.TextField()

    def __str__(self):
        return self.email



class Comment(models.Model):
    body         = models.TextField()
    user         = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    news         = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
    active       = models.BooleanField(default=True)

    class Meta:
        ordering = ['created_time']
    
    def __str__(self):
        return f"Comment - {self.body} by {self.user}"
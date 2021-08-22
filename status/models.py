from django.db import models
from django.contrib.auth.models import User


def upload_status_image(instance, filename):
    return f'status-media/{instance.user}/{filename}'


class StatusQuerySet(models.QuerySet):
    pass


class StatusManager(models.Manager):
    def get_queryset(self):
        return StatusQuerySet(self.model, using=self._db)


class Status(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to=upload_status_image, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    object = StatusManager()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Status Post'
        verbose_name_plural = 'Status Posts'

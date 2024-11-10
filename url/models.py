from django.db import models


class Url(models.Model):
    url = models.CharField(max_length=250, blank=False, null=False)
    key = models.CharField(unique=True, max_length=50, blank=False, null=False)
    views = models.PositiveIntegerField(default=0, blank=False, null=False)

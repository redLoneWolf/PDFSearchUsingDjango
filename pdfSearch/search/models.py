from django.db import models
import os
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Search(models.Model):
    keyText = models.TextField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ('-created',)


class Pics(models.Model):

    image = models.TextField(blank=False)
    search =  models.ForeignKey(Search, on_delete=models.CASCADE)
    pdf = models.TextField(blank=False)
    page = models.IntegerField(blank=False)
    created = models.DateTimeField(auto_now_add=True)
    


from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext as _
# import secrets
import random as secrets  # BUG - Necessary for PYTHON <3.6


class Timestamp(models.Model):
    YEAR = 'year'
    MONTH = 'month'
    DAY = 'day'
    SECOND = 'second'
    PRECISION = [
        (YEAR, _('year')),
        (MONTH, _('month')),
        (DAY, _('day')),
        (SECOND, _('second')),
    ]
    status = models.CharField(
        max_length=10,
        choices=PRECISION,
        default=SECOND,
    )


class Location(models.Model):
    name = models.CharField(null=True, max_length=50,)
    description = models.TextField(null=True, max_length=10000)
    coords = models.CharField(null=True, max_length=30)  # GPS coords
    osmObject = models.CharField(null=True, max_length=30)  # OpenStreetMap object ID (city...)


class PhotoMetadata(models.Model):
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    timestamp = Timestamp()


# Create your models here.
class Photo(models.Model):
    urlkey = models.CharField(null=True, max_length=30)  # If generated, key used for sharing the photo as a URL
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    filename = models.ImageField()
    models.OneToOneField(PhotoMetadata, on_delete=models.SET_NULL, null=True, blank=True)

    @staticmethod
    def generateFileName(name="DSC.jpg"):
        """Returns a random-prefixed file name from the uploaded file name"""
        return secrets.token_hex(10) + '_' + name


class Album(models.Model):
    urlkey = models.CharField(null=True, max_length=30)  # If generated, key used for sharing the photo as a URL
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    # Content
    photos = models.ManyToManyField(Photo)
    # Metadata
    name = models.CharField(null=True, max_length=150)
    description = models.TextField(null=True, max_length=10000)
    location = models.ManyToManyField(Location)
    startTime = Timestamp()
    endTime = Timestamp()

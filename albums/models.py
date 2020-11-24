# ManikAlbum, an online collaborative editor of family photo albums
#    Copyright (C) 2020  Manik Bhattacharjee <manik.bhattacharjee <at> free.fr>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, version 3 of the
#    License.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

#from django.contrib.auth.models import User
from django.utils.translation import gettext as _
from django.contrib.auth.models import AbstractUser
from django.db import models

# import secrets
import random as secrets  # FIXME BUG - Necessary for PYTHON <3.6

class User(AbstractUser):
    description = models.TextField(max_length=1000)
    personalUrl = models.URLField()
    pass

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
    """
    Define a photo album, which is a collection of photos

    It has metadata (name, description, location, datetime)
    It has access rights: an owner (creator) and members with Permissions
     e.g. (Read-only, add-only, read-write, admin)
    """
    public = models.BooleanField(null=False, default=False)  # Anonymous user has read access
    urlkey = models.CharField(null=True, max_length=30)  # If generated, key used for sharing the photo as a URL
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")
    admins = models.ManyToManyField(User, related_name="admins")
    members = models.ManyToManyField(User, related_name="members")
    # Content
    photos = models.ManyToManyField(Photo)
    # Metadata
    name = models.CharField(null=True, max_length=150)
    description = models.TextField(null=True, max_length=10000)
    location = models.ManyToManyField(Location)
    startTime = Timestamp()
    endTime = Timestamp()

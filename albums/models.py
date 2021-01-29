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
from django.urls import reverse
from django.dispatch import receiver

# import secrets
import secrets
import os
from datetime import datetime


class User(AbstractUser):
    description = models.TextField(max_length=1000,blank=True,null=True)
    personalUrl = models.URLField(blank=True, null=True)
    is_admin = models.BooleanField('admin status', default=False)
    def __str__(self):
        return AbstractUser.__str__(self)


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    shortName = models.CharField(max_length=20)
    fullName = models.CharField(null=True, max_length=20, blank=True)
    birthDate = models.DateField(null=True, blank=True)
    deathDate = models.DateField(null = True, blank=True)

    def get_absolute_url(self):
        return reverse('personview', args=[str(self.id)])

    def __str__(self):
        return self.shortName


class Metadata(models.Model):
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
    timedetail = models.CharField(
        max_length=10,
        choices=PRECISION,
        default=SECOND,
    )
    timestamp = models.DateTimeField(blank=True, null=True)
    #timestamp = models.OneToOneField(Timestamp, null=True, blank=True,on_delete=models.SET_NULL)
    name = models.CharField(blank =True, max_length=50, )
    description = models.TextField(blank=True, max_length=10000)
    #TODO Exif metadata fields ? Class EXIF from django-exiffield ?
    persons = models.ManyToManyField('Person', through='PersonPresence')
    locations = models.ManyToManyField('Location', through='LocationPresence')
    def __str__(self):
        return "Meta: " + self.name


class PersonPresence(models.Model):
    person = models.ForeignKey(Person, on_delete=models.SET_NULL, blank=True, null=True) #blank -> there is someone unknown
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE)
    x = models.FloatField(blank=False, default=0.0)
    y = models.FloatField(blank=False, default=0.0)
    w = models.FloatField(blank=False, default=1.0)
    h = models.FloatField(blank=False, default=1.0)
    tStart = models.TimeField(blank=True, null=True)
    tEnds = models.TimeField(blank=True, null=True)

    def __str__(self):
        return self.person.shortName + " present in " + self.metadata.name


class Location(models.Model):
    name = models.CharField(max_length=50,null=True)
    description = models.TextField(blank=True, max_length=10000, null=True)
    parentLocation = models.ForeignKey('Location', on_delete=models.SET_NULL, blank=True, null=True)
    coords = models.CharField(blank=True, max_length=100, null=True)  # GPS coords TODO GeoDjango ?
    osmObject = models.CharField(blank=True, max_length=100, null=True)  # OpenStreetMap object ID (city...)

    def get_absolute_url(self):
        return reverse('locationview', args=[str(self.id)])

    def __str__(self):
        return self.name


class LocationPresence(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=False)
    metadata = models.ForeignKey(Metadata, on_delete=models.CASCADE, blank=False)
    tStart = models.TimeField(blank=True,null=True)
    tEnds = models.TimeField(blank=True,null=True)

    def __str__(self):
        return self.location.name + " is location for " + self.metadata.name


def generateRandomKey():
    return secrets.token_hex(10)


def generateFilePath(instance, filename):
    """Returns a random-prefixed file name from the uploaded file name"""
    _now = datetime.now()
    return 'photos/u-{0}/{1}/{2}/{3}/{4}'.format(instance.owner.id, _now.year, _now.month, _now.day, filename)

class Photo(models.Model):
    # If generated, key used for sharing the photo as a URL
    urlkey = models.CharField(null=True, max_length=30,default=generateRandomKey)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    filename = models.ImageField(upload_to=generateFilePath)
    thumbnail = models.ImageField(blank=True,null=True)
    metadata = models.OneToOneField(Metadata, on_delete=models.CASCADE)
    public = models.BooleanField(null=False, default=False) # anonymous user has read access ?

    def get_absolute_url(self):
        return reverse('photoview', args=[str(self.id)])

    def __str__(self):
        return self.filename.name


@receiver(models.signals.post_delete, sender=Photo)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file and thumbnail from filesystem
    when corresponding `Photo` object is deleted.
    """
    if instance.filename:
        if os.path.isfile(instance.filename.path):
            os.remove(instance.filename.path)
    if instance.thumbnail:
        if os.path.isfile(instance.thumbnail.path):
            os.remove(instance.thumbnail.path)

@receiver(models.signals.pre_save, sender=Photo)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file and thumbnail from filesystem
    when corresponding `Photo` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Photo.objects.get(pk=instance.pk).filename
        old_thumb = Photo.objects.get(pk=instance.pk).thumbnail
    except Photo.DoesNotExist:
        return False

    new_file = instance.filename
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
        if old_thumb:
            if os.path.isfile(old_thumb.path):
                os.remove(old_thumb.path)



class PhotoIndex(models.Model):
    album = models.ForeignKey("Album",on_delete=models.CASCADE)
    photo = models.ForeignKey(Photo,on_delete=models.CASCADE)
    index = models.IntegerField(default=-1)

    class Meta:
        unique_together = (("album", "photo", "index"),)


class Album(models.Model):
    """
    Define a photo album, which is a collection of photos

    It has metadata (name, description, location, datetime)
    It has access rights: an owner (creator) and members with Permissions
     e.g. (Read-only, add-only, read-write, admin)
    """
    public = models.BooleanField(null=False, default=False)  # Anonymous user has read access
    # If generated, key used for sharing the photo as a URL
    urlkey = models.CharField(null=True, max_length=30, default=generateRandomKey)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="owner")
    admins = models.ManyToManyField(User, related_name="admins")
    members = models.ManyToManyField(User, related_name="members")
    # Content
    photos = models.ManyToManyField(Photo, through=PhotoIndex)
    # Metadata
    name = models.CharField(null=True, max_length=150)
    description = models.TextField(null=True, max_length=10000)
    location = models.ManyToManyField(Location)
    startTime = models.DateField(null=True, blank=True)
    endTime = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('albumview', args=[str(self.id)])

    def __str__(self):
        return "Album " + self.name


# TODO Add lock model with user, datetime info that can be applied to album, photo, metadata, location or person

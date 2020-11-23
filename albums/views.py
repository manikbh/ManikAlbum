from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView

from .models import Album

# Create your views here.
def index(request):
    return HttpResponse("Index de l'application Album.")

# Managing your account (mail, password, name)
def account(request):
    pass
# Managing a group (adding and removing members and admins)
def group(request):
    pass
# Managing your photos (uploads, select into albums or for metadata edit)
def browse(request):
    pass
# View a photo
def photo(request):
    pass
def myAlbums(request):
    pass
# View an Album
def album(request):
    pass
# Edit metadata of a photo (must have an account)
def photoMetadata(request):
    pass
# Edit an album and its metadata (add/remove photos)
def albumEdit(request):
    pass
# People FoF relationships, full name, short name, date of birth/death
def peopleEdit(request):
    pass
# Locations (name, map, sublocation of)
def locationEdit(request):
    pass


class AlbumListView(ListView):
    model = Album
    def myAlbums(self):
        return Album.objects.filter(owner=self.request.user).order_by('start_datetime')  #.filter(status__exact='o')
    def head(self, *args, **kwargs):
        last_book = self.get_queryset().latest('publication_date')
        response = HttpResponse()
        # RFC 1123 date format
        response['Last-Modified'] = last_book.publication_date.strftime('%a, %d %b %Y %H:%M:%S GMT')
        return response

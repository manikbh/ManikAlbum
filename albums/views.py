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

from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Album, User, Photo, Location, Person
from .forms import SignUpForm


def index(request):
    if request.user.is_authenticated:
        return HttpResponse("Index de l'application Album.<br/><a href='myalbums/'>My Albums</a>")
    else:
        return HttpResponse("Index de l'application Album.<br/><a href='login/'>Login</a>")


class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'


    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('myAlbums')


# Managing your account (mail, password, name)
@login_required
def account(request):
    return HttpResponse("My account")


# Managing a group (adding and removing members and admins)
@login_required
def group(request):
    return HttpResponse("Manage group")


# Managing your photos (uploads, select into albums or for metadata edit)
def browse(request):
    pass


# View a photo
def photo(request,photo_id):
    try:
        photoUrl = Photo.objects.get(pk=photo_id).filename.url
        # TODO Use CSS Hover to make click zone visible
        # https://stackoverflow.com/questions/8343531/is-it-possible-to-style-a-mouseover-on-an-image-map-using-css
        return HttpResponse("Viewing Photo " + str(photo_id) + "<br/><img src=\"" + photoUrl
                            + "\" style=\"width: 55vw; min-width: 330px;\" usemap=\"#facesmap\">"
                            + "<map name=\"facesmap\">"
                            + "<area shape=\"rect\" coords=\"0,0,10,150\" alt=\"Person shortname\" href=\"/peopleview/1/\"></map>")
    except:
        return HttpResponse("Viewing Photo " + str(photo_id) + "<br/><b>NOT FOUND</b>")

@login_required
def myAlbums(request):
    album_list = Album.objects.filter(owner=request.user).order_by('name')
    context = {
        'album_list': album_list,
    }
    return render(request, 'albums/myalbums.html', context=context)  # View an Album


def albumView(request, album_id, photo_index=-1):
    if photo_index < 0:
        #Full album view
        return HttpResponse("Viewing album " + str(album_id) + " -> all photos")
    else:
        return HttpResponse("Viewing album " + str(album_id) + ", photo index="+str(photo_index))


# Edit metadata of a photo (must have an account)
def photoMetadata(request):
    pass


# Edit an album and its metadata (add/remove photos)
@login_required
def albumEdit(request, album_id):
    pass


# People FoF relationships, full name, short name, date of birth/death
def peopleEdit(request):
    pass

# People in pictures
def peopleView(request,person_id):
    return HttpResponse("Looking at person "+str(person_id))



# Locations (name, map, sublocation of)
def locationEdit(request):
    pass


class AlbumListView(ListView):
    template_name = "albums/myalbums.html"
    model = Album
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user).order_by('name')  # .filter(status__exact='o')

class AlbumDetailView(DetailView):
    model = Album
    template_name = "albums/album.html"

class PhotoDetailView(DetailView):
    model = Photo
    template_name = "albums/photo.html"

class LocationDetailView(DetailView):
    model = Location
    template_name = "albums/location.html"

class PersonDetailView(DetailView):
    model = Person
    template_name = "albums/person.html"


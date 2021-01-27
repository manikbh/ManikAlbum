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
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, CreateView, DetailView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from django.urls import reverse

from PIL import Image, ExifTags
from datetime import datetime
import os
import json

from urllib.parse import urlparse

from .models import Album, User, Photo, Location, Person, Metadata
from .forms.SignUpForm import SignUpForm
from .forms.photouploadform import PhotoUploadForm


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

# @login_required
# def myAlbums(request):
#     album_list = Album.objects.filter(owner=request.user).order_by('name')
#     context = {
#         'album_list': album_list,
#     }
#     return render(request, 'albums/myalbums.html', context=context)  # View an Album
#
#
# def albumView(request, album_id, photo_index=-1):
#     if photo_index < 0:
#         #Full album view
#         return HttpResponse("Viewing album " + str(album_id) + " -> all photos")
#     else:
#         return HttpResponse("Viewing album " + str(album_id) + ", photo index="+str(photo_index))
#



class PhotoListView(ListView):
    template_name = "albums/myphotos.html"
    model = Album
    context_object_name = 'photo_list'

    def get_queryset(self):
        startAt = 0
        maxElements = 20
        if 'startAt' in self.kwargs:
            startAt = self.kwargs['startAt']
        if 'maxElements' in self.kwargs:
            maxElements = self.kwargs['maxElements']

        return Photo.objects.filter(owner=self.request.user).order_by('id')[startAt:startAt+maxElements]  # .filter(status__exact='o')


class AlbumListView(ListView):
    template_name = "albums/myalbums.html"
    model = Album
    context_object_name = 'album_list'

    def get_queryset(self):
        return Album.objects.filter(owner=self.request.user).order_by('name')  # .filter(status__exact='o')


class LocationListView(ListView):
    template_name = "albums/mylocations.html"
    model = Location
    context_object_name = 'album_list'
    paginate_by = 2
#    def get_queryset(self): # TODO filter only those that the user has access to
#        return Album.objects.filter(owner=self.request.user).order_by('name')  # .filter(status__exact='o')


class PersonListView(ListView):
    template_name = "albums/mypersons.html"
    model = Person
    context_object_name = 'album_list'

#    def get_queryset(self): # TODO filter only those that the user has access to
#        return Album.objects.filter(owner=self.request.user).order_by('name')  # .filter(status__exact='o')


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


# Forms
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LocationCreateUpdateView(LoginRequiredMixin, UpdateView):
    model = Location
    fields = ['name', 'description', 'parentLocation', 'coords', 'osmObject']
    success_url = reverse_lazy('mylocations') # TODO MyLocations, list of all locations the user has access to
    #pk = None

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def form_valid(self, form):
        # form.instance.created_by = self.request.user
        # item = form.save()
        # self.pk = item.pk
        return super().form_valid(form)

    #def get_success_url(self):
    #     #print(self.pk)
    #     return reverse_lazy('locationsview', kwargs={'pk': self.pk})


# People FoF relationships, full name, short name, date of birth/death
class PersonCreateUpdateView(LoginRequiredMixin, UpdateView):
    model = Person
    fields = ['shortName', 'fullName', 'birthDate', 'user']
    success_url = reverse_lazy('mypersons')  # TODO MyLocations, list of all locations the user has access to
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None


class AlbumCreateUpdateView(LoginRequiredMixin, UpdateView):
    model = Album
    fields = ['name', 'description', 'location', 'startTime', 'endTime',
              'public', 'photos', 'owner', 'admins', 'members', 'urlkey']
    success_url = reverse_lazy('myalbums')
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

@require_http_methods(["POST"])
def albumCreateAPI(request):
    is_ajax = request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest
    data = json.load(request)
    print("Received create album request: " + repr(data))
    albumname = "DefaultName"
    if albumname in data:
        albumname = data['albumname']
    if 'images' not in data:
        return HttpResponseBadRequest
    try:
        if Album.objects.filter(name=albumname).count() > 0:
            return JsonResponse({'error': "album name already exists", })
        album = Album(name=albumname, owner=request.user)
        album.save()
        album.photos.add(*[int(p[6:]) for p in data['images']])
        album.save()
        return JsonResponse({'success': "album %s was created"%albumname, })
    except:
        return JsonResponse({'error': "album creation failed on server", })

class PhotoCreateUpdateView(LoginRequiredMixin, UpdateView):
    model = Photo
    #  Update also metadata in the same view, may need django extension
    #  https://stackoverflow.com/questions/26200674/updateview-update-a-class-that-has-onetoone-with-user
    fields = ['filename', 'thumbnail', 'metadata', 'owner', 'urlkey', 'public']
    #success_url = reverse_lazy('myalbums')  # TODO Or ju
    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except AttributeError:
            return None

    def get_success_url(self):
        return reverse_lazy('photoview', kwargs={'pk': self.pk})


class PhotoDeleteView(DeleteView):
    model = Photo
    success_url = reverse_lazy('myalbums')


class AlbumDeleteView(DeleteView):
    model = Album
    success_url = reverse_lazy('myalbums')


class LocationDeleteView(DeleteView):
    model = Location
    success_url = reverse_lazy('mylocations')


class PersonDeleteView(DeleteView):
    model = Person
    success_url = reverse_lazy('mypersons')


def uploadPhoto(request,albumpk=-1):
    def remove_prefix(text, prefix):
        if text.startswith(prefix):
            return text[len(prefix):]
        return text  # or whatever

    # Handle file upload
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES)
        if form.is_valid():
            for upFile in request.FILES.getlist('file'):
                metadata = Metadata(name=upFile.name)
                metadata.save()
                newPhoto = Photo(owner=request.user, filename=upFile, metadata=metadata)
                # Save the photo file in the path from chunks
                newPhoto.save()
                newPhotoPath = newPhoto.filename.path
                # Create a thumbnail
                size = 250, 250
                filename, ext = os.path.splitext(newPhotoPath)
                im = Image.open(newPhotoPath)
                im.thumbnail(size)
                if im._getexif() is not None and 36867 in im._getexif():  # DateTimeOriginal
                    exifdate = datetime.strptime(im._getexif()[36867], '%Y:%m:%d %H:%M:%S')
                else:
                    exifdate = None
                thumbfile = filename + "_thumb.jpg"
                im.save(thumbfile, "JPEG", quality=70)
                newPhoto.thumbnail.name = remove_prefix('.'.join(urlparse(newPhoto.filename.url).path.split('.')[:-1]) + "_thumb.jpg", "/media/")
                newPhoto.save()  # Save thumbnail

                # Update Metadata and populate it (name, exif date and GPS coords, description)
                metadata.timestamp=exifdate
                metadata.save()


                # If there is an album pk, add the photo to it:
                if form.cleaned_data['albumpk'] >= 0:
                    print("There is an albumpk -> "+repr(form.cleaned_data['albumpk']))
                    if Album.objects.filter(pk=form.cleaned_data['albumpk']).exists():
                        Album.objects.get(pk=albumpk).photos.add(newPhoto)
                else:
                    print("There is NO albumpk -> "+repr(form.cleaned_data['albumpk']))


            # Redirect to the document list after POST
            return JsonResponse({'error': False, 'message': "<br/>".join([upFile.name + ' uploaded !' for upFile in request.FILES.getlist('file')])})
            #return HttpResponseRedirect(reverse('myalbums'))
        else:
            return JsonResponse({'error': True, 'errors': form.errors})
    else:
        print("Creating photo upload form with albumpk="+repr(albumpk))
        form = PhotoUploadForm(initial={'albumpk': albumpk})  # A empty, unbound form

    # GET
    return render(request,
                  'albums/photouploader.html',
                  {'form': form, 'albumpk': albumpk}
                  )

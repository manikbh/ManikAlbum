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
from django.views.generic import ListView, CreateView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .models import Album, User
from .forms import SignUpForm

# Create your views here.
def index(request):
    return HttpResponse("Index de l'application Album.")

class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('students:quiz_list')

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
def photo(request):
    pass
def myAlbums(request):
    album_list = []
    if request.user.is_authenticated:
        album_list = Album.objects.filter(owner = request.user).order_by('-startTime')
    template = loader.get_template('albums/myalbums.html')
    context = {
        'album_list': album_list,
    }
    return render(context, request)# View an Album

def album(request, album_id):
    pass
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

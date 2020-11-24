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

from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('group', views.group, name='group'),
    path('photo', views.photo, name='photo'),
    path('browse', views.browse, name='browse'),
    path('myalbums', views.myAlbums, name='myAlbums'),
    path('albumview/<int:album_id>', views.album, name='albumview'),
    path('albumedit/<int:album_id>', views.albumEdit, name='albumEdit'),
    path('peopleedit', views.peopleEdit, name='peopleEdit'),
    path('locationedit', views.locationEdit, name='locationEdit'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
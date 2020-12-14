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
    #path('photo/<int:photo_id>', views.photo, name='photo'),
    path('photo/<int:pk>', views.PhotoDetailView.as_view(), name='photoview'),
    path('browse', views.browse, name='browse'),
    #path('myalbums/', views.myAlbums, name='myAlbums'),
    path('myalbums/', views.AlbumListView.as_view(), name='myAlbums'),
    #path('albumview/<int:album_id>/', views.albumView, name='albumview'),
    path('albumview/<int:pk>/', views.AlbumDetailView.as_view(), name='albumview'),
    path('albumview/<int:album_id>/<int:photo_index>/', views.albumView, name='albumviewphoto'),
    path('albumedit/<int:album_id>/', views.albumEdit, name='albumEdit'),
    path('personview/<int:pk>/', views.PersonDetailView.as_view(), name='personview'),
    path('personedit/<int:person_id>/', views.peopleEdit, name='personedit'),
    path('personcreate/', views.PersonCreateView.as_view(), name='personcreate'),
    path('locationview/<int:pk>/', views.LocationDetailView.as_view(), name='locationview'),
    path('locationedit/<int:pk>/', views.locationEdit, name='locationedit'),
    path('locationcreate/', views.LocationCreateView.as_view(), name='locationcreate'),
]

# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if settings.DEBUG:
#         urlpatterns += staticfiles_urlpatterns("albums/")
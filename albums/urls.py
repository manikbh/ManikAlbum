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
    path('signup/', views.account, name='signup'),
    path('account/', views.account, name='account'),
    path('login/', views.account, name='maniklogin'),
    path('logout/', views.account, name='maniklogout'),
    path('group', views.group, name='group'),
    #  path('photo/<int:photo_id>', views.photo, name='photo'),
    path('photo/<int:pk>', views.PhotoDetailView.as_view(), name='photoview'),
    path('photoedit/<int:pk>/', views.PhotoCreateUpdateView.as_view(), name='photoedit'),
    path('photodelete/<int:pk>/', views.PhotoDeleteView.as_view(), name='photodelete'),
    path('browse', views.browse, name='browse'),
    #  path('myalbums/', views.myAlbums, name='myAlbums'),
    path('myalbums/', views.AlbumListView.as_view(), name='myalbums'),
    path('mylocations/', views.LocationListView.as_view(), name='mylocations'),
    path('mypersons/', views.PersonListView.as_view(), name='mypersons'),
    #  path('albumview/<int:album_id>/', views.albumView, name='albumview'),
    path('albumview/<int:pk>/', views.AlbumDetailView.as_view(), name='albumview'),
    path('albumview/<int:album_id>/<int:photo_index>/', views.albumView, name='albumviewphoto'),
    path('albumedit/<int:pk>/', views.AlbumCreateUpdateView.as_view(), name='albumedit'),
    path('albumcreate/', views.AlbumCreateUpdateView.as_view(), name='albumcreate'),
    path('albumdelete/<int:pk>/', views.AlbumDeleteView.as_view(), name='albumdelete'),
    path('personview/<int:pk>/', views.PersonDetailView.as_view(), name='personview'),
    path('personedit/<int:pk>/', views.PersonCreateUpdateView.as_view(), name='personedit'),
    path('personcreate/', views.PersonCreateUpdateView.as_view(), name='personcreate'),
    path('persondelete/<int:pk>/', views.PersonDeleteView.as_view(), name='persondelete'),
    path('locationview/<int:pk>/', views.LocationDetailView.as_view(), name='locationview'),
    path('locationedit/<int:pk>/', views.LocationCreateUpdateView.as_view(), name='locationedit'),
    path('locationcreate/', views.LocationCreateUpdateView.as_view(), name='locationcreate'),
    path('locationdelete/<int:pk>/', views.LocationDeleteView.as_view(), name='locationdelete'),
]

# from django.conf import settings
# from django.conf.urls.static import static
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# if settings.DEBUG:
#         urlpatterns += staticfiles_urlpatterns("albums/")

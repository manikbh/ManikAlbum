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
import django.contrib.auth.views as auth_views

from . import views

urlpatterns = [
    path('', views.AlbumListView.as_view(), name='index'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('account/', views.AccountView.as_view(), name='account'),
    path('login/', auth_views.LoginView.as_view(), {'next_page': '/'}, name='maniklogin'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page': '/'}, name='maniklogout'),
    path('group', views.group, name='group'),
    #  path('photo/<int:photo_id>', views.photo, name='photo'),
    path('photo/<int:pk>', views.PhotoDetailView.as_view(), name='photoview'),
    path('photoedit/<int:pk>/', views.PhotoCreateUpdateView.as_view(), name='photoedit'),
    path('photocreate/', views.PhotoCreateUpdateView.as_view(), name='photocreate'),
    path('photodelete/<int:pk>/', views.PhotoDeleteView.as_view(), name='photodelete'),
    path('myphotos/<int:startAt>/', views.PhotoListView.as_view(), name='myphotos'),
    path('myphotos/', views.PhotoListView.as_view(), name='myphotos'),
    path('photoupload/', views.uploadPhoto, name='photoupload'),
    path('photoupload/<int:albumpk>/', views.uploadPhoto, name='photoupload'),
    path('myalbums/', views.AlbumListView.as_view(), name='myalbums'),
    path('mylocations/', views.LocationListView.as_view(), name='mylocations'),
    path('mypersons/', views.PersonListView.as_view(), name='mypersons'),
    path('albumview/<int:pk>/', views.AlbumDetailView.as_view(), name='albumview'),
    # path('albumview/<int:pk>/<int:photo_index>/', views.albumDetailView.as_view(), name='albumviewphoto'),
    path('albumedit/<int:pk>/', views.AlbumCreateUpdateView.as_view(), name='albumedit'),
    path('albumcreate/', views.AlbumCreateUpdateView.as_view(), name='albumcreate'),
    path('albumcreate2/', views.albumCreateAPI, name='albumcreate2'),
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

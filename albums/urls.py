from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('account', views.account, name='account'),
    path('group', views.group, name='group'),
    path('photo', views.photo, name='photo'),
    path('browse', views.browse, name='browse'),
    path('myalbums', views.AlbumListView.as_view(), name='myAlbums'),
    path('albumview', views.album, name='album'),
    path('albumedit', views.albumEdit, name='albumEdit'),
    path('peopleedit', views.peopleEdit, name='peopleEdit'),
    path('locationedit', views.locationEdit, name='locationEdit'),
]

from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)
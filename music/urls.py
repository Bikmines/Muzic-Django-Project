from django.conf.urls import url
from django.contrib.auth.views import login, logout
from music import views
from music.models import Album

app_name='music'

urlpatterns = [
    url(r'^$', views.Indexview.as_view() ,name="index"),
    url(r'^register/$', views.userformview.as_view() ,name="register"),
    url(r'^(?P<pk>[0-9]+)/$', views.Detailview.as_view() ,name="detail"),
    url(r'^album/add/$', views.Albumcreate.as_view(), name="album-add"),
    url(r'^album/(?P<album>[0-9]+)/addsong/$', views.addsong.as_view(), name="addsong"),
    url(r'^album/(?P<album>[0-9]+)/favorite/$',views.favorite, name="favorite"),
    url(r'^song/$', views.songs.as_view(), name="song"),
    url(r'^album/(?P<pk>[0-9]+)/$', views.Albumupdate.as_view(), name="albumupdate"),
    url(r'^album/(?P<pk>[0-9]+)/delete/$', views.Albumdelete.as_view(), name="albumdelete"),
    url(r'^album/(?P<pk>[0-9]+)/songdelete/$', views.songdelete.as_view(), name="songdelete"),
    url(r'^logout/$', views.logout_view,name="logout"),
    url(r'^login/$', views.login_view,name="login"),
    url(r'^profile/(?P<pk>[0-9]+)/$', views.ProfileView.as_view(), name="user_profile"),
    url(r'^profile/(?P<pk>[0-9]+)/request/$', views.FriendRequestView.as_view(), name="friend_request"),
]

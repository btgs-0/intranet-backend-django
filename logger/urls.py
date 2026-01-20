"""logger URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  re_path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  re_path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  re_path(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include
from django.contrib import admin
from rest_framework import routers, permissions
# Source - https://stackoverflow.com/a
# Posted by masnun, modified by community. See post 'Timeline' for change history
# Retrieved 2026-01-20, License - CC BY-SA 3.0
from rest_framework.authtoken import views as auth_views
from playlist import views
from session.views import UserViewSet, MigrateAndLogin
from catalogue.views import ReleaseViewSet, TrackViewSet, ArtistViewSet, CommentViewSet
from downloads import views as downloadViews
from supporters import views as supporterViews
from django.urls import re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Three D Radio Backend API",
      default_version='v1',
      #description="",
      #terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="tech@threedradio.com"),
      #license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'releases', ReleaseViewSet, 'release')
router.register(r'tracks', TrackViewSet, 'track')
router.register(r'artists', ArtistViewSet, 'Artist')
router.register(r'comments', CommentViewSet, 'Comment')

router.register(r'shows', views.ShowViewSet, 'Show')
router.register(r'users', UserViewSet, 'user')
router.register(r'playlists', views.PlaylistViewSet, 'Playlist')
router.register(r'playlistentries', views.PlaylistEntryViewSet,
                'PlaylistEntry')

router.register(r'supporters', supporterViews.SupporterViewSet, 'Supporter')
router.register(r'transactions', supporterViews.TransactionViewSet, 'Transaction')

urlpatterns = [
    re_path(r'^api-token-auth/', auth_views.obtain_auth_token),
    re_path(r'^auth', MigrateAndLogin.as_view()),
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^api/', include(router.urls)),
    re_path(r'^logger/', include('playlist.urls')),
    re_path(r'^download/([a-f0-9\-]+)', downloadViews.download),
    re_path(r'^swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
]

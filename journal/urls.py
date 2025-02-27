from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("archive", views.archive, name="archive"),
    path("login", views.login, name='login'),
    path("logout", views.logout, name='logout'),
    # path("upload/", views.upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("journal/", views.homepage, name="homepage"),
    path("journal/archive", views.archive, name="archive"),
    path("journal/login", views.login, name='login'),
    path("journal/logout", views.logout, name='logout'),
    # path("upload/", views.upload, name="upload"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
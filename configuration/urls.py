from django.contrib import admin
from django.shortcuts import redirect
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from campingapp.views import CampingListView


urlpatterns = [
    path("admin/", admin.site.urls),
    path("camping/", include("campingapp.urls")),
    path("", CampingListView.as_view(), name="index"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

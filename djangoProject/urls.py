from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("bbsh_api/", include("bbsh_api.urls")),
]

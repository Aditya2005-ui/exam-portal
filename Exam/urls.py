from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),

    # mcq app urls
    path("", include("mcq.urls")),
]
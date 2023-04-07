from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('members/', include('django.contrib.auth.urls')),
    path('members/', include('members.urls')),


    path('', include('bookmarks_main.urls')),
    path('admin/', admin.site.urls),
]

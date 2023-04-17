from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-main'),
    path('bookmarks', views.userhome, name='home-page'),
    path('delete_bookmark/<str:id>', views.delete_bookmark, name='delete-bookmark'),
    path('edit_bookmark/<str:id>', views.edit_bookmark, name='edit-bookmark'),
    path('contact', views.contact, name='contact'),
    path('get_favicon', views.get_favicon, name='get_favicon'),
]

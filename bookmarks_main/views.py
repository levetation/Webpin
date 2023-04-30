from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Saved_Bookmarks
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.decorators import login_required

from members import views

## favicon imports
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests

from django.http import HttpResponse

## ChatGPT favicon function
def get_favicon_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    favicon_url = None
    for link in soup.find_all('link'):
        if link.get('rel') == ['shortcut', 'icon'] or link.get('rel') == ['icon']:
            favicon_url = link.get('href')
            break
    if favicon_url:
        parsed_favicon_url = urlparse(favicon_url)
        if not parsed_favicon_url.scheme:
            parsed_url = urlparse(url)
            base_url = parsed_url.scheme + "://" + parsed_url.netloc
            favicon_url = urljoin(base_url, favicon_url)
    return favicon_url

## ChatGPT view
def get_favicon(request):
    url = request.GET.get('url')
    favicon_url = get_favicon_url(url)
    if favicon_url:
        response = requests.get(favicon_url)
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        return HttpResponse(status=404)

## Legacy favicon URL grabber
def favicon_url(url):
    url_list = url.split('/')
    if len(url_list) >= 1:
        fav_url = f"{url_list[0]}//{url_list[2]}/favicon.ico"
        return fav_url

@login_required(login_url="/members/login_user")
def userhome(request):
    context = {}

    # gets bookmarks
    bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id).order_by('-bookmark_save_date')

    ## delete all bookmarks
    all_user_bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id)

    # checks to display button
    all_user_bookmarks_list = list(all_user_bookmarks)
    if len(all_user_bookmarks_list) >= 1: context['all_user_bookmarks_list'] = True

    if request.method == 'POST' and 'delete_all_bookmarks' in request.POST:
        all_user_bookmarks.delete()
        return redirect(request.META['HTTP_REFERER'])
 
    context['bookmarks'] = bookmarks

    if bookmarks.exists():
        context['bookmark_exist'] = 'User has bookmarks'

    # get all unique catagories from user bookmarks
    bookmark_list = [bookmark for bookmark in bookmarks]
    catagories = list(set([entry.bookmark_catagory for entry in bookmark_list if entry.bookmark_catagory != '']))
    context['catagories'] = catagories

    if request.method =='POST' and 'select_catagory' in request.POST:
        bookmarks = Saved_Bookmarks.objects.filter(
            bookmark_catagory=request.POST['selected_bookmark_catagory'],
            author=request.user.id
        ).order_by('-bookmark_save_date')
        
        context['bookmarks'] = bookmarks
        return render(request, 'bookmarks_main/index.html', context)

    elif request.method =='POST' and 'view_all' in request.POST:
        return redirect(request.META['HTTP_REFERER'])

    if request.method == 'POST' and 'submit_new_bookmark' in request.POST:

        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        new_bookmark_catagory = request.POST['new_bookmark_catagory']

        new_bookmark = Saved_Bookmarks(
            bookmark_title = new_bookmark_title,
            bookmark_address = new_bookmark_address,
            bookmark_notes = new_bookmark_notes,
            bookmark_catagory = new_bookmark_catagory,
            author = request.user,
        )

        new_bookmark.save()
        # return HttpResponseRedirect('')
        return redirect(request.META['HTTP_REFERER'])

    return render(request, 'bookmarks_main/index.html', context)

## delete bookmark
@login_required(login_url="/members/login_user")
def delete_bookmark(request, id):
    bookmark_checked = Saved_Bookmarks.objects.get(pk=id)
    bookmark_checked.delete()
    return redirect('home-page')

## edit bookmark
@login_required(login_url="/members/login_user")
def edit_bookmark(request, id):
    bookmark_to_edit = Saved_Bookmarks.objects.get(pk=id)

    if request.method == 'POST' and 'submit_edit_selected_bookmark' in request.POST:

        new_bookmark_title = request.POST['new_bookmark_title']
        new_bookmark_address = request.POST['new_bookmark_address']
        new_bookmark_notes = request.POST['new_bookmark_notes']
        new_bookmark_catagory = request.POST['new_bookmark_catagory']

        bookmark_update = Saved_Bookmarks.objects.filter(pk=id).update(
            bookmark_title=new_bookmark_title,
            bookmark_address=new_bookmark_address,
            bookmark_notes=new_bookmark_notes,
            bookmark_catagory=new_bookmark_catagory
            )

        messages.success(request, ("Bookmark updated"))
        return redirect(request.META['HTTP_REFERER'])

    elif request.method == 'POST' and 'delete_selected_bookmark' in request.POST:

        bookmark_to_edit.delete()

        return redirect('home-page')

    return render(request, 'bookmarks_main/edit.html', {'bookmark_to_edit':bookmark_to_edit})

def home(request):
    return render(request, 'bookmarks_main/welcome.html', {})

def contact(request):
    return render(request, 'bookmarks_main/contact.html', {})

def devblog(request):
    return render(request, 'bookmarks_main/devblog.html', {})
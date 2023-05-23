from django.shortcuts import render, redirect
from .models import Saved_Bookmarks
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

## favicon imports
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import requests
from django.http import HttpResponse
from django.core.cache import cache


## webscrape for favicon url
def get_favicon_url(url):

    # creates cache key
    cache_key = f'favicon_{url}'

    # checks for url in cache
    favicon_url = cache.get(cache_key)
    if favicon_url:
        return favicon_url
    
    # generates favicon from url
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
        # puts url in cache
        cache.set(cache_key, favicon_url)
    return favicon_url

## Grab the favicon url for the page
def get_favicon(request):
    url = request.GET.get('url')
    cache_key = f'favicon_{url}'
    favicon_url = cache.get(cache_key)
    if not favicon_url:
        favicon_url = get_favicon_url(url)
    if favicon_url:
        cache.set(cache_key, favicon_url)
        response = requests.get(favicon_url)
        return HttpResponse(response.content, content_type=response.headers['Content-Type'])
    else:
        return HttpResponse(status=404)

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
        if request.POST['selected_bookmark_catagory'] == 'View all':
            redirect(request.META['HTTP_REFERER'])
        else:
            bookmarks = Saved_Bookmarks.objects.filter(
                bookmark_catagory=request.POST['selected_bookmark_catagory'],
                author=request.user.id
            ).order_by('-bookmark_save_date')

        context['bookmarks'] = bookmarks
        return render(request, 'bookmarks_main/index.html', context)

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

@login_required(login_url="/members/login_user")
def account_settings(request):
    context = {}

    ## delete all bookmarks
    all_user_bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id)

    ## checks to display button
    all_user_bookmarks_list = list(all_user_bookmarks)
    # if list is > or = to 1
    if len(all_user_bookmarks_list) >= 1: context['all_user_bookmarks_list'] = True

    context['bookmarks_len'] = len(all_user_bookmarks_list)

    ## delete all bookmarks button
    if request.method == 'POST' and 'delete_all_bookmarks' in request.POST:
        all_user_bookmarks.delete()
        return redirect(request.META['HTTP_REFERER'])
 
    return render(request, 'bookmarks_main/account_settings.html', context)

def bookmark_list_download(request):
    response = HttpResponse(content_type = 'text/plain')
    response['Content-Disposition'] = 'attachment; filename=webpin_bookmarks.html'

    ## delete all bookmarks
    all_user_bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id).order_by('-bookmark_save_date')

    ## checks to display button
    all_user_bookmarks_list = []
    for bookmark in all_user_bookmarks:
        # write bookmarks to html code making it readable to browsers
        all_user_bookmarks_list.append(f'<a href={bookmark.bookmark_address}>{bookmark.bookmark_title}</a><br>')
        # all_user_bookmarks_list.append(f'<p>{bookmark.bookmark_notes}</p><br>')

    response.writelines(all_user_bookmarks_list)
    return response


from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from .models import Saved_Bookmarks
from django.contrib.auth.models import User
from django.contrib import messages
import requests, time

## Get favicon from any url
def favicon_url(url):
    url_list = url.split('/')
    if len(url_list) >= 1: 
        fav_url = f"{url_list[0]}//{url_list[2]}/favicon.ico"
        return fav_url 
        
# Create your views here.
def userhome(request):
    context = {}
    
    # gets bookmarks
    start = time.time()
    bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id).order_by('-bookmark_save_date')
    end = time.time()
    print("Bookmark load time:", end-start)
    ## delete all bookmarks
    all_user_bookmarks = Saved_Bookmarks.objects.filter(author=request.user.id)
    
    # checks to display button
    all_user_bookmarks_list = list(all_user_bookmarks)
    if len(all_user_bookmarks_list) >= 1: context['all_user_bookmarks_list'] = True

    if request.method == 'POST' and 'delete_all_bookmarks' in request.POST:
        all_user_bookmarks.delete()
        return redirect(request.META['HTTP_REFERER'])
        

    # favicon url list

    # start = time.time()
    favicon_urls = []
    default_address = 'https://www.webpin.co.uk/static/bookmarks_main/webpin_pin.PNG'
    for bookmark in bookmarks:
        if bookmark.bookmark_address:
            fav_url = favicon_url(bookmark.bookmark_address)
            response = requests.head(fav_url)
            if response.status_code != 200:
                favicon_urls.append(default_address)
            else:
                favicon_urls.append(fav_url)
        else:
            favicon_urls.append(default_address)

    # end = time.time()
    # print('Favicon load time:', end-start)
    
    bookmarks_and_urls = zip(bookmarks, favicon_urls)
    
    context['bookmarks'] = bookmarks_and_urls 
   
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

        favicon_urls = [favicon_url(bookmark.bookmark_address) for bookmark in bookmarks]
        bookmarks_and_urls = zip(bookmarks, favicon_urls)
        context['bookmarks'] = bookmarks_and_urls
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

def delete_bookmark(request, id):
    bookmark_checked = Saved_Bookmarks.objects.get(pk=id)
    bookmark_checked.delete()
    return redirect('home-page')

## edit bookmark

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
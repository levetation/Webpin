from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

@login_required
def notes_home(request):
    return render(request, 'notes/notes_home.html', {})

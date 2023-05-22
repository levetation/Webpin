from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import RegisterUserForm
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required


def login_user(request):
	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			# Redirect to a success page.
			return redirect('home-page')
		else:
			# Return an 'invalid login' error message.
			messages.success(request, ("error for login in"))
			return redirect('login')
	else:
		return render(request, 'authenticate/login.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, ("You were logged out"))
	return redirect('home-main')

def register_user(request):
	if request.method == "POST":
		form = RegisterUserForm(request.POST) # registerUserForm is from forms.py
		if form.is_valid():
			form.save()
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			messages.success(request, ('registration successful'))
			return redirect('home-page')
	else:
		form = RegisterUserForm()

	return render(request, 'authenticate/register_user.html', {'form':form,})

@login_required(login_url="/members/login_user")
def user_profile(request):
	if request.user.is_authenticated:
		context = {'user_object':request.user}
	return render(request, 'authenticate/user_profile.html', context)

@login_required(login_url="/members/login_user")
def update_profile(request):
	if request.user.is_authenticated:
		current_user = User.objects.get(id=request.user.id)
		form = RegisterUserForm(request.POST or None, instance=current_user)
		if form.is_valid():
			form.save()
			login(request, current_user)
			messages.success(request, ("Your profile has been updated"))
			return redirect('user_profile')
		context = {'form':form}
		return render(request, 'authenticate/update_profile.html', context)




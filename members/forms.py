from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

class RegisterUserForm(UserCreationForm):
	
	username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter a username'}), label='')
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Enter your email'}), label='')
	password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password'}), label='')
	password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Please re-enter your password', 'data-toggle': 'password'}), label='')

	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2')

	# beautifying username, password1, & password2
	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)

		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'


class UserDeleteForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [] # Form only needs 'submit' button. However, fields still necessary
		
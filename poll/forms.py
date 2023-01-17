from django import forms
from . models import Poll, CompleteRegistration
from django.contrib.auth.models import  User
class RegistrationForm(forms.Form):
	username = forms.CharField(max_length=200, label='Full name')
	# email = forms.EmailField()
	password = forms.CharField(max_length=30, widget=forms.PasswordInput())
	confirm = forms.CharField(max_length=30, widget=forms.PasswordInput())

	def clean_username(self):
		try:
			User.objects.get(username=self.cleaned_data['username'])
		except User.DoesNotExist:
			return self.cleaned_data['username']
		raise forms.ValidationError("This name already exist, try another name, or login if you have already register")

	def clean(self):
		if 'password' in self.cleaned_data and 'confirm' in self.cleaned_data:
			if self.cleaned_data['password'] != self.cleaned_data['confirm']:
				raise forms.ValidationError('Password confirmation did not match, try again')
		return self.cleaned_data

	def save(self):
		new_user = User.objects.create_user(username=self.cleaned_data['username'], 
			password=self.cleaned_data['password'])
		return new_user
		
class Polls(forms.ModelForm):
	class Meta:
		model = Poll
		exclude = ["vote_count", "have_vote"]

class CompleteRegistrations(forms.ModelForm):
	class Meta:
		model = CompleteRegistration
		fields = "__all__"
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.models import User
from django.contrib import messages
from . import models as models_forms, forms as forms_forms


complete = models_forms.CompleteRegistration.objects.all()

def please_login(request):
	return render(request, 'poll/please_login.html')

def registration_close(request):
	return render(request, 'poll/close.html')

def show_r(request):
	return render(request, 'poll/show_r.html')

def already(request):
	return render(request, 'poll/already.html')

def vote_home(request):
	if request.user.is_authenticated and not request.user.is_superuser:
		if complete:
			try:
				request.user != request.user.completeregistration.relation
			except:
				return redirect('complete_registration')
		else:
			return redirect('complete_registration')

	position = models_forms.Position.objects.all()
	try:
		admin = models_forms.AdminSitting1.objects.get(pk=1)
	except:
		models_forms.AdminSitting1.objects.create(
			start_vote=False,
			registration_complete=False,
			show_results=False,
			be_inform="Welcom"
			)
		return redirect('poll_board')
	display_info = admin.be_inform
	contact_info = admin.contact

	if request.method == "POST":
		display = request.POST.get('display_info')
		admin.be_inform = display

		contact = request.POST.get('contact')
		admin.contact = contact

		start_vote = request.POST.get('start_vote')
		registration_complete = request.POST.get('registration_complete')
		show_results = request.POST.get('show_results')
		if start_vote == 'on':
			admin.start_vote = True
		else:
			admin.start_vote = False

		if registration_complete == 'on':
			admin.registration_complete = True
		else:
			admin.registration_complete = False

		if show_results == 'on':
			admin.show_results = True
		else:
			admin.show_results = False
		admin.save()
		return redirect('poll_board')
	return render(request, 'poll/vote_home.html', {"contact_info": contact_info, "display_info": display_info, "position": position, "admin": admin,})

def messages_section(request):
	if request.user.is_authenticated and not request.user.is_superuser:
		if complete:
			if request.user != request.user.completeregistration.relation:
				return redirect('complete_registration')
		else:
			return redirect('complete_registration')

	messages = models_forms.Messages.objects.all()
	if request.method == "POST":
		if request.user.is_authenticated:
			models_forms.Messages.objects.create(
				user=request.user, message=request.POST.get('message'))
			return redirect('messages')
		else:
			return redirect('please_login')
	return render(request, 'poll/messages.html', {"messages": messages})

@login_required(login_url='please_login')
def delete_message(request, message_id):
	page = 'delete'
	message = get_object_or_404(models_forms.Messages, pk=message_id)
	if request.user != message.user:
		return redirect('messages')

	else:
		message.delete()
		return redirect('messages')
	return render(request, 'poll/messages.html', {"page": page})

@login_required(login_url='please_login')
def create_poll(request):
	if not request.user.is_superuser:
		return HttpResponse("<h2>Sorry, Administrators only</h2>")
	page = 'create_poll'
	position = models_forms.Position.objects.all()
	form = forms_forms.Polls
	if request.method == "POST":
		form = forms_forms.Polls(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('poll_board')
	context = {"form": form, "position": position, 'page': page}
	return render(request, 'poll/create_poll.html', context)

@login_required(login_url='please_login')
def vote(request):
	q = request.GET.get('q')
	poll = models_forms.Poll.objects.filter(person_position__person_position__icontains=q)
	for n in poll:
		if request.user == n.have_vote:
			return redirect('already')
	return render(request, 'poll/vote.html', {"poll": poll, "q": q})

@login_required(login_url='please_login')
def submit_vote(request, poll_id):
	admin = models_forms.AdminSitting1.objects.get(pk=1)
	if admin.start_vote == False:
		return HttpResponse('<h2>ICT master have not start the vote yet </h2>')
	if request.user.is_authenticated and not request.user.is_superuser:
		if request.user.completeregistration.can_vote == False:
			return HttpResponse("<h2>Sorry, ICT master have not allow you to vote</h2>")
		if complete:
			if request.user != request.user.completeregistration.relation:
				return redirect('complete_registration')
		else:
			return redirect('complete_registration')

	q = request.GET.get('q')
	poll = get_object_or_404(models_forms.Poll, pk=poll_id)
	polls = models_forms.Poll.objects.filter(person_position__person_position__icontains=q)
	for n in polls:
		if request.user == n.have_vote:
			return HttpResponse("<h1>Sorry you have already vote in these section, go to the next section to vote</h1>")

	if request.method == "POST":
		if request.user.is_superuser:
			return HttpResponse("<h2>Admin I don't think you can vote.</h2>")
		poll.have_vote = request.user
		poll.vote_count += 1
		poll.save()
		messages.success(request, "You vote was submit successfully, you can go to the next section to vote.")
		return redirect('poll_board')
	return render(request, 'poll/submit_vote.html', {"poll": poll})


def result_home(request):
	admin = models_forms.AdminSitting1.objects.get(pk=1)
	if admin.show_results == False:
		return redirect('show_r')
	position = models_forms.Position.objects.all()
	return render(request, 'poll/result_home.html', {"position": position})

def results(request):
	admin = models_forms.AdminSitting1.objects.get(pk=1)
	if admin.show_results == False:
		return HttpResponse("<h2>Sorry, ICT master have not show the results</h2>")
		
	q = request.GET.get('q')
	poll = models_forms.Poll.objects.filter(person_position__person_position__icontains=q)
	return render(request, 'poll/result.html', {"poll": poll, "q": q})

def about(request):
	return render(request, 'poll/about.html')

def voters(request):
	all_users = User.objects.all()[1:]
	if request.method == "POST":
		for user in all_users:
			user.delete()
			return redirect('voters')
	if request.user.is_authenticated and not request.user.is_superuser:
		if complete:
			if request.user != request.user.completeregistration.relation:
				return redirect('complete_registration')
		else:
			return redirect('complete_registration')

	q = request.GET.get('q') if request.GET.get('q') != None else ""
	student_range = models_forms.StudentRange.objects.all()

	voters = models_forms.CompleteRegistration.objects.filter(
		Q(student_range__student_range__icontains=q) |
		Q(your_course__student_course__icontains=q) |
		Q(phone_number__icontains=q) |
		Q(relation__username__icontains=q)
		)
	phone_num = ""
	for phone in voters:
		phone_num = phone.phone_number[:6] + "####"
	course = models_forms.StudentCourse.objects.all()
	return render(request, 'poll/voters.html', {"voters": voters, "q": q, "student_range": student_range, "course": course, "phone_num": phone_num,  "all_users": all_users})

def delete_poll(request):
	if not request.user.is_superuser:
		return HttpResponse("<h2>Sorry, you are not allow here! Admin only.</h2>")

	q = request.GET.get('q') if request.GET.get('q') != '' else ""
	poll = models_forms.Poll.objects.filter(person_position__person_position__icontains=q)
	if request.method == "POST":
		poll.delete()
		return redirect('poll_board')
	return render(request, 'poll/delete_poll.html', {'poll': poll, "q": q})

def can_vote(request, person_id):
	voters = get_object_or_404(models_forms.CompleteRegistration, pk=person_id)
	if request.method == "POST":
		can_vote = request.POST.get('can_vote')
		if can_vote == 'on':
			voters.can_vote = True
		if can_vote == None:
			voters.can_vote = False
		voters.save()
		return redirect('voters')
	return render(request, 'poll/can_vote.html', {"voters": voters})

@login_required(login_url='please_login')
def logout_user(request):
	logout(request)
	messages.success(request, "successfully logout, goodbye")
	return redirect('poll_board')

def register_user(request):
	admin = models_forms.AdminSitting1.objects.get(pk=1)
	if admin.registration_complete == True:
		return redirect('registration_close')
	if request.user.is_authenticated:
		return redirect('poll_board')

	form =forms_forms.RegistrationForm
	user_pass = None
	if request.method == "POST":
		form = forms_forms.RegistrationForm(data=request.POST)
		if form.is_valid():
			p = request.POST.get('password')
			user = form.save()
			user.username = user.username.lower()
			user.last_name=p

			user.save()
			login(request, user)
			return redirect("complete_registration")
	return render(request, 'poll/registration.html', {'form': form})


def login_page(request):
	if request.user.is_authenticated:
		return redirect('poll_board')

	tel = models_forms.AdminSitting1.objects.get(pk=1).contact
	form = AuthenticationForm
	if request.method == "POST":

		if form.is_valid:
			username = request.POST.get('login_username')
			password = request.POST.get('login_password')

			if username != 'ICT-Master':
				username = username.lower()
			

			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f"Hi, Welcome back {username}", request.user)
			else:
				messages.error(request, "Sorry username and password did not match, try again")
				

			if request.user.is_authenticated:
				return redirect('poll_board')
		else:
			messages.error(request, "Sorry username and password did not match, try again")

	return render(request, 'poll/login.html', {'tel': tel})

@login_required(login_url='please_login')
def complete_registration(request):
	form = forms_forms.CompleteRegistrations
	if request.method == "POST":
		form = forms_forms.CompleteRegistrations(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('poll_board')
	return render(request, 'poll/complete_register.html', {"form": form})

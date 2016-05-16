from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django import forms
from .models import Claim
from .forms import PostForm

def claim_list(request, type=' '):
	if not type == ' ':
		claims = Claim.objects.filter(type=type).order_by('-upvotes')
	else:
		claims = Claim.objects.order_by('-upvotes')
	return render(request, 'survey/claim_list.html', {'claims': claims})
	
@login_required
def claim_detail(request, pk, type=' '):
	claim = get_object_or_404(Claim, pk=pk)
	#check for button presses
	if request.user not in claim.voters.all():
		if request.GET.get("upvote"):
			claim.upvotes = claim.upvotes + 1 
			claim.voters.add(request.user)
		if request.GET.get("downvote"):
			claim.downvotes = claim.downvotes + 1 
			claim.voters.add(request.user)
	if request.user not in claim.answerers.all():		
		if request.GET.get("yea"):
			claim.yeas = claim.yeas + 1 
			claim.answerers.add(request.user)
		if request.GET.get("nay"):
			claim.nays = claim.nays + 1 
			claim.answerers.add(request.user)
		
	claim.save()
	return render(request, 'survey/claim_detail.html', {'claim': claim})

@login_required
def claim_new(request, type = ' '):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			claim = form.save(commit=False)
			if request.user.is_authenticated():
				claim.author = request.user
			else:
				claim.author = None
			claim.yeas = 0
			claim.nays = 0
			claim.upvotes = 1
			claim.downvotes = 0
			if not type == ' ':
				claim.type = type
			claim.save()
			claim.voters.add(request.user)
			claim.save()
			return redirect('claim_detail', pk=claim.pk)
	else:
		form = PostForm()
	return render(request, 'survey/claim_new.html', {'form': form})
	
def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			user = authenticate(username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password1'))	#I pulled this off the internet, no idea why you need cleaned-data or "password1"
			login(request, user)
			return redirect('claim_list')
	else:
		form = UserCreationForm()
	return render(request, "registration/register.html", {'form': form,})
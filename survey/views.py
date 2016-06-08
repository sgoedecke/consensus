from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django import forms
from .models import Claim
from .forms import PostForm

@login_required
def claim_vote(request, pk, type = ' '):
	claim = get_object_or_404(Claim, pk=pk)
	claim.upvotes = claim.upvotes + 1 
	claim.voters.add(request.user)

	claim.save()
	return render(request, '/survey/claim_list.html') #REDIRECTS TO /phil/


def claim_list(request, vote = ' ', pk=0, type=False):

	#handle weird setting of type to '1' so urls recognises it
	
	if request.user.is_authenticated():
		if type == '1':
			viewing_category = "philosophy"
			type = True
		elif type == '0':
			viewing_category = " "
		else:
			viewing_category = request.user.profile.viewing
	
		if request.user.profile.viewing != viewing_category:
			request.user.profile.switch()
	else:
		if type == '1':
			viewing_category = "philosophy"
			type = True
		else:
			viewing_category = " "


	#handle votes if needed
	if request.user.is_authenticated():
		if vote != ' ':
			claim = get_object_or_404(Claim,pk=pk)
			type = claim.type
			if request.user not in claim.voters.all():
				if vote == 'upvote':
					claim.upvotes = claim.upvotes + 1 
					claim.voters.add(request.user)
				if vote == 'downvote':
					claim.downvotes = claim.downvotes + 1 
					claim.voters.add(request.user)
			if request.user not in claim.answerers.all():		
				if vote == 'yea':
					claim.yeas = claim.yeas + 1 
					claim.answerers.add(request.user)
				if vote == 'nay':
					claim.nays = claim.nays + 1 
					claim.answerers.add(request.user)
			claim.save()

				
	#display claim list
	if request.user.is_authenticated():

		user_profile = request.user.profile
		user_viewing = user_profile.viewing
	else:
		user_viewing = viewing_category
	if user_viewing == "philosophy":
		print "******** GETTING PHIL CLAIMS ****"
		claims = Claim.objects.filter(type=True).order_by('-score')
	else:
		claims = Claim.objects.order_by('-score')
	print type
	return render(request, 'survey/claim_list.html', {'claims': claims})
	
@login_required
def claim_detail(request, pk, type=False):
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
def claim_new(request):
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

def about(request):
	return render(request, "survey/about.html")

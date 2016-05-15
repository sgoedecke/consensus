from django.shortcuts import render, get_object_or_404, redirect
from .models import Claim
from .forms import PostForm

def claim_list(request):
	claims = Claim.objects.order_by('-upvotes')
	return render(request, 'survey/claim_list.html', {'claims': claims})
	
def claim_detail(request, pk):
	claim = get_object_or_404(Claim, pk=pk)
	#check for button presses
	if request.GET.get("upvote"):
		claim.upvotes = claim.upvotes + 1 
	if request.GET.get("downvote"):
		claim.downvotes = claim.downvotes + 1 
	if request.GET.get("yea"):
		claim.yeas = claim.yeas + 1 
	if request.GET.get("nay"):
		claim.nays = claim.nays + 1 
		
	claim.save()
	return render(request, 'survey/claim_detail.html', {'claim': claim})
	
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
            return redirect('claim_detail', pk=claim.pk)
    else:
        form = PostForm()
    return render(request, 'survey/claim_new.html', {'form': form})
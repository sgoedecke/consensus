from django.shortcuts import render, get_object_or_404, redirect
from .models import Claim
from .forms import PostForm

def claim_list(request):
	claims = Claim.objects.order_by('upvotes')
	return render(request, 'survey/claim_list.html', {'claims': claims})
	
def claim_detail(request, pk):
	claim = get_object_or_404(Claim, pk=pk)
	return render(request, 'survey/claim_detail.html', {'claim': claim})
	
def claim_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)
            claim.author = poster
            claim.yeas = 0
            claim.nays = 0
            claim.upvotes = 1
            claim.downvotes = 0
            claim.save()
            return redirect('claim_detail', pk=claim.pk)
    else:
        form = PostForm()
    return render(request, 'survey/claim_new.html', {'form': form})
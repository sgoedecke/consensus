from django import forms
from .models import Claim

class PostForm(forms.ModelForm):
	class Meta:
		model = Claim
		fields = ('text',)
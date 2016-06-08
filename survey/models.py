from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.



class Claim(models.Model):
	author = models.ForeignKey('auth.User', null=True) #allows for no author
	text = models.CharField(max_length=600)
	created_date = models.DateTimeField(default=timezone.now)
	yeas = models.IntegerField()
	nays = models.IntegerField()
	upvotes = models.IntegerField()
	downvotes = models.IntegerField()
	type = models.BooleanField("Is this philosophy?")	#Yes for phil, no for empty
	
	voters = models.ManyToManyField(User, related_name='+')
	answerers = models.ManyToManyField(User, related_name='+')
	
	def publish(self):
		self.save()
		
	def __str__(self):
		return self.text
		

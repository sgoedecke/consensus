from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


# Create your models here.

class UserProfile(models.Model):
	user = models.ForeignKey(User, unique=True)
	viewing = models.CharField(max_length=100, blank=True)
	
	def switch(self):
		if self.viewing == " ":
			self.viewing = "philosophy"
		else:
			self.viewing = " "
		self.save()
		
	def __str__(self):
		return self.user
		
User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0]) #magic to auto-create a UP


class Claim(models.Model):
	author = models.ForeignKey('auth.User', null=True) #allows for no author
	text = models.CharField(max_length=600)
	created_date = models.DateTimeField(default=timezone.now)
	yeas = models.IntegerField()
	nays = models.IntegerField()
	upvotes = models.IntegerField()
	downvotes = models.IntegerField()
	score = models.IntegerField(default=0)
	type = models.BooleanField("Is this philosophy?", default=True)	#Yes for phil, no for empty  SET as true for BP people
	
	voters = models.ManyToManyField(User, related_name='+')
	answerers = models.ManyToManyField(User, related_name='+')
	
	def save(self):
		self.score = (self.yeas + self.nays) - (2 * self.downvotes)
		super(Claim,self).save()
	
	def publish(self):
		self.save()
		
	def __str__(self):
		return self.text
		

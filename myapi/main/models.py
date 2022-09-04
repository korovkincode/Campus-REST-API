from django.db import models

class Restaurant(models.Model):
	username = models.CharField(max_length = 30, unique = True)
	password = models.CharField(max_length = 20)
	menu = models.CharField(max_length = 300)
	voted = models.CharField(max_length = 10 ** 3)
	liked = models.IntegerField(default = 0)
	disliked = models.IntegerField(default = 0)

	def __str__(self):
		return self.username

class Employee(models.Model):
	username = models.CharField(max_length = 20, unique = True)
	password = models.CharField(max_length = 20)

	def __str__(self):
		return self.username
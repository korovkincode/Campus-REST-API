from rest_framework import serializers
from .models import Restaurant, Employee

class RestaurantSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Restaurant
		fields = ('username', 'password', 'menu', 'voted', 'liked', 'disliked')
		extra_kwargs = {'password': {'write_only': True}, 'voted': {'read_only': True}, 'liked': {'read_only': True}, 'disliked': {'read_only': True}}

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Employee
		fields = ('username', 'password')
		extra_kwargs = {'password': {'write_only': True}}

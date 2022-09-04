import pytest
from rest_framework.test import APIClient

client = APIClient()

@pytest.mark.django_db
def test_register_user():
	credentials = {
	'username': 'test',
	'password': '12345'
	}
	assert client.post('/api/user/register', credentials).data == {'message': 'New user registered!'}
	assert client.post('/api/user/register', credentials).data == {'message': 'Error!'}
	assert client.post('/api/user/login', credentials).data == {'message': 'User logged in'}

@pytest.mark.django_db
def test_register_rest():
	credentials = {
	'username': 'KFC',
	'password': '123',
	'menu': 'Chicken Bucket'
	}
	assert client.post('/api/rest/register', credentials).data == {'message': 'New restaurant registered!'}
	assert client.post('/api/rest/login', credentials).data == {'message': 'Restaurant logged in'}
	assert client.get('/api/rest/KFC/stats').data == {'disliked': 0, 'liked': 0}
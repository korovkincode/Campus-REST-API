from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RestaurantSerializer, EmployeeSerializer
from .models import Employee, Restaurant
import jwt

class UserRegisterView(APIView):
	def post(self, request):
		if not request.COOKIES.get('userinfo'):
			try:
				serializer = EmployeeSerializer(data = request.data)
				serializer.is_valid(raise_exception = True)
				serializer.save()
				return Response({'message': 'New user registered!'})
			except:
				return Response({'message': 'Error!'})
		return Response({'message': 'You has already logged in'})

class UserLoginView(APIView):
	def post(self, request):
		username = request.data['username']
		password = request.data['password']

		user = Employee.objects.filter(username = username, password = password).first()
		if user is not None:
			response = Response()
			userinfo = jwt.encode({'username': username, 'password': password}, 'secret', algorithm = 'HS256')
			response.set_cookie(key = 'userinfo', value = userinfo, httponly = True)
			response.data = {'message': 'User logged in'}
			return response

		return Response({'message': 'Not found!'})

class UserView(APIView):
	def get(self, request):
		if request.COOKIES.get('userinfo'):
			try:
				userinfo = jwt.decode(request.COOKIES.get('userinfo'), 'secret', algorithms = ['HS256'])
				username = userinfo['username']
				password = userinfo['password']
				user = Employee.objects.filter(username = username, password = password).first()
				return Response({'username': username, 'password': password})
			except:
				return Response({'message': 'Error!'})
		return Response({'message': 'No user logged in!'})

class UserVoteView(APIView):
	def post(self, request, restname):
		if request.COOKIES.get('userinfo'):
			try:
				userinfo = jwt.decode(request.COOKIES.get('userinfo'), 'secret', algorithms = ['HS256'])
				username = userinfo['username']
				vote = request.data['vote']
				rest = Restaurant.objects.filter(username = restname).first()
				if username not in rest.voted.split(';'):
					if vote == 'Like':
						rest.liked += 1
						rest.voted += username + ';'
					elif vote == 'Dislike':
						rest.disliked += 1
						rest.voted += username + ';'
				else:
					return Response({'message': 'User has already voted for this menu!'})
				rest.save()
				return Response({'message': 'User voted successfully!'})
			except:
				return Response({'message': 'Error!'})
		return Response({'message': 'No user logged in!'})

class UserLogoutView(APIView):
	def get(self, request):
		response = Response()
		response.delete_cookie('userinfo')
		response.data = {'message': 'User logged out'}
		return response

class RestRegisterView(APIView):
	def post(self, request):
		serializer = RestaurantSerializer(data = request.data)
		serializer.is_valid(raise_exception = True)
		serializer.save()
		return Response({'message': 'New restaurant registered!'})

class RestLoginView(APIView):
	def post(self, request):
		username = request.data['username']
		password = request.data['password']

		user = Restaurant.objects.filter(username = username, password = password).first()
		if user is not None:
			response = Response()
			userinfo = jwt.encode({'username': username, 'password': password}, 'secret', algorithm = 'HS256')
			response.set_cookie(key = 'restinfo', value = userinfo, httponly = True)
			response.data = {'message': 'Restaurant logged in'}
			return response

		return Response({'message': 'Not found!'})

class RestView(APIView):
	def get(self, request):
		if request.COOKIES.get('restinfo'):
			try:
				restinfo = jwt.decode(request.COOKIES.get('restinfo'), 'secret', algorithms = ['HS256'])
				username = restinfo['username']
				password = restinfo['password']
				user = Restaurant.objects.filter(username = username, password = password).first()
				return Response({'username': username, 'password': password, 'menu': RestaurantSerializer(user).data['menu'],
				'voted': RestaurantSerializer(user).data['voted'], 'liked': RestaurantSerializer(user).data['liked'],
				'disliked': RestaurantSerializer(user).data['disliked']})
			
			except:
				return Response({'message': 'Error!'})
		return Response({'message': 'No restaurant logged in!'})

class RestGetMenuView(APIView):
	def get(self, request, restname):
		try:
			rest = Restaurant.objects.filter(username = restname).first()
			return Response({'menu': RestaurantSerializer(rest).data['menu']})
		except:
			return Response({'message': 'Error!'})

class RestGetStatsView(APIView):
	def get(self, request, restname):
		try:
			rest = Restaurant.objects.filter(username = restname).first()
			return Response({'liked': RestaurantSerializer(rest).data['liked'], 'disliked': RestaurantSerializer(rest).data['disliked']})
		except:
			return Response({'message': 'Error!'})

class RestSetMenuView(APIView):
	def post(self, request):
		if request.COOKIES.get('restinfo'):
			try:
				restinfo = jwt.decode(request.COOKIES.get('restinfo'), 'secret', algorithms = ['HS256'])
				username = restinfo['username']
				password = restinfo['password']
				menu = request.data['menu']
				user = Restaurant.objects.filter(username = username, password = password).first()
				user.menu = menu
				user.voted = ''
				user.liked = 0
				user.disliked = 0
				user.save()
				return Response({'username': username, 'password': password, 'menu': menu, 'voted': '', 'liked': 0, 'disliked': 0})
			except:
				return Response({'message': 'Error!'})
		return Response({'message': 'No restaurant logged in!'})

class RestLogoutView(APIView):
	def get(self, request):
		response = Response()
		response.delete_cookie('restinfo')
		response.data = {'message': 'Restaurant logged out'}
		return response
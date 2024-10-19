from django.contrib.auth import authenticate
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .serializers import UserSerializer
from base64 import b64encode
from rest_framework.authtoken.models import Token

class RegisterView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer

class LoginView(APIView):
	def post(self, request):
		username = request.data.get("username")
		password = request.data.get("password")
		user = authenticate(request, username=username, password=password)
		if user is not None:
			token, created = Token.objects.get_or_create(user=user)

			base_string = f'{username}:{token.key}'
			encoded_token = b64encode(base_string.encode()).decode()

			response = Response({"message": "Login successful!"}, status=200)
			response['Authorization'] = f'Basic {encoded_token}'

			return response
		return Response({"error": "Invalid credentials"}, status=400)

class LogoutView(APIView):
	def post(self, request):
		return Response({"message": "Logout successful!"}, status=200)

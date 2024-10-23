from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .serializers import UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class RegisterAPIView(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	permission_classes = (permissions.AllowAny,)

	def perform_create(self, serializer):
		serializer.save(password=serializer.validated_data['password'])


class ObtainTokenPairView(APIView):
	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')

		try:
			user = User.objects.get(email=email)
		except User.DoesNotExist:
			return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

		user = authenticate(request, username=user.username, password=password)

		if user is not None:
			refresh = RefreshToken.for_user(user)
			return Response({
				'refresh': str(refresh),
				'access': str(refresh.access_token),
			})
		else:
			return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutAPIView(APIView):
	def post(self, request):
		try:
			refresh_token = request.data['refresh_token']
			token = RefreshToken(refresh_token)
			token.blacklist()

			return Response(status=status.HTTP_205_RESET_CONTENT)
		except Exception as e:
			return Response(status=status.HTTP_400_BAD_REQUEST)

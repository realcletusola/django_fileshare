import asyncio 
import logging 
from datetime import timedelta
from django.utils import timezone 
from django.contrib.auth import authenticate, get_user_model  
from django.db.models import Q 
from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework_simplejwt.tokens import RefreshToken 

from .serializers import SignUpSerializer, SignInSerializer
from .database import database 

User = get_user_model()

# initialize logger
logger = logging.getLogger('authentication')

# signup view 
class SignUpRequest(APIView):

	# set permission and serializer classes
	permission_classes = [permissions.AllowAny, ]
	serializer_class = SignUpSerializer

	# handle post request for user registration 
	async def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)

			if serializer.is_valid(raise_exception=True):
				# use async context manager to handle database connection 
				async with database.transaction():
					await asyncio.to_thread(serializer.save)

				# return success response 
				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "Account created."
				})

			else:
				# return error response 
				return Response({
					"status": "error",
					"status_code": status.HTTP_400_BAD_REQUEST,
					"details": serializer.errors,
					"error_message": "Request failed. Invalid data format."
				})

		except Exception as e:
			logger.error(f"An error occurred in user signup request: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occured. Please try again later."
			})



# signin view 
class SignInRequest(APIView):

	# set permission and serializer classes
	permission_classes = [permissions.AllowAny, ]
	serializer_class = SignInSerializer


	# handle post request for user signin 
	async def post(self, request):
		serializer = self.serializer_class(data.request.data)

		if serializer.is_valid(raise_exception=True):
			loginId = serializer.validated_data["login_id"]
			password = serializer.validated_data["password"]

			user = await asyncio.to_thread(authenticate(request, username=loginId, password=password))

			if user is not None:
				if user.is_active:
					refresh = RefreshToken.for_user(user) # generate refresh token for user
					await asyncio.to_thread(user.reset_login_trials()) # reset login trials 

					# return success response 
					return Response({
						"status": "success",
						"status_code": status.HTTP_200_OK,
						"access": str(refresh.access_token),
						"refresh": str(refresh),
						"details": "Login successful."
					})

				# if user is not active 
				else:
					# return error response 
					return Response({
						"status": "error",
						"status_code": status.HTTP_401_UNAUTHORIZED,
						"details": "Account not active. Please contact our support team."
					})

			# if user is None (failed authentication)
			else:
				try:
					# try to find user with the provided login id (username or email) 
					user = await asyncio.to_thread(User.objects.get, (Q(username__iexact=loginId) | Q(email__iexact=loginId)))
					if user:
						# get user last failed login time
						if user.last_failed_login:
							time_since_last_failed_login = timezone.now() - user.last_failed_login
							# if time_since_last_failed_login is > 24 (24 hours), reset user login_trials
							if time_since_last_failed_login > timedelta(hours=24):
								await asyncio.to_thread(user.reset_login_trials())

						# if user hasn't exceeded the login trials 
						if user.login_trials < user.max_login_trials:
							await asyncio.to_thread(user.increment_login_trials()) # add 1 to the current login trial count
							# return invalid username or password response 
							return Response({
								"status": "error",
								"status_code": status.HTTP_401_UNAUTHORIZED,
								"details": "Invalid login credentials."
							})

						# if login_trials is > max_login_trials
						else:
							return Response({
								"status": "error",
								"status_code": status.HTTP_401_UNAUTHORIZED,
								"details": "You've tried too many times. Please try again after 24 hours"
							})

					# if no user is found 
					else:
						return Response({
							"status": "error",
							"status_code": status.HTTP_401_UNAUTHORIZED,
							"details": "Invalid login credentials."
						})

				except Exception as e:
					logger.error(f"An error occured in user signin request: {e}", exc_info=True)
					return Response({
						"status": "error",
						"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
						"details": "An error occurred. Please try again later."
					})

		# if serializer is not valid 
		else:
			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Authentication request failed. Invalid data format or credentials."
			})


# signout view 
class SignOutRequest(APIView):

	# set permissions class
	permission_classes = [permissions.IsAuthenticated]

	async def post(self, request):
		# try to get token from http header 
		try:
			authorization_header = request.headers.get('Authorization')
			token = None

			if authorization_header:
				# split authorization header into part (token should be in Bearer <token>)
				parts = authorization_header.split()

				# if length of part is 2 
				if len(parts) == 2:
					token = parts[1]

			if token:
				# blacklist refresh token 
				refresh_token = RefreshToken(token)
				refresh_token.blacklist()

				# return success response
				return Response({
					"status": "success",
					"status_code": status.HTTP_204_NO_CONTENT,
					"details": "Logout successful."
				})

			else:
				# get refresh token from form data if token is not provided in authentication header
				refresh_token = request.data["refresh"]

				if refresh_token:
					# blacklist token 
					token = RefreshToken(refresh_token)
					token.blacklist()
					
					# return success response 
					return Response({
						"status": "success",
						"status_code": status.HTTP_204_NO_CONTENT,
						"details": "Logout successful"
					})

				else:
					return Response({
						"status": "error",
						"status": status.HTTP_401_UNAUTHORIZED,
						"details": "Unable to log you out. Please provide a valid token"
					})

		except Exception as e:
			except Exception as e:
				logger.error(f"An error occurred in user signout request: {e}", exc_info=True)
				return Response({
					"status":"error",
					"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
					"details": "An error occurred. Please try again later."
				})







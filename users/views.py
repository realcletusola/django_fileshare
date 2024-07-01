import asyncio 
import logging 
from django.db.models import Q 
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import (
	ProfileSerializer, FileSerializer,
	FileOperationSerializer, UserSerializer
)
from fileshare.database import database 
from .models import Profile, File, FileOperation

User = get_user_model()

# initialize logger
logger = logging.getLogger('users')


# profile view 
class ProfileRequest(APIView):
	permissions_classes = [permissions.IsAuthenticated, ]
	serializer_class = ProfileSerializer

	# profile queryset to get profile based on the permissions of the user 
	async def get_queryset(self):
		user = self.request.user 
		try:
			if user.is_staff or user.is_superuser:
				return await asyncio.to_thread(Profile.objects.all)

			profile = await asyncio.to_thread(Profile.objects.get, user=user)
			return profile

		except Profile.DoesNotExist:
			raise Http404("Profile does not exist")

		except Exception as e:
			logger.error(f"An error occurred on user profile queryset: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred in getting user profile."
			})


	async def get(self, request):
		try:
			profile = await self.get_queryset()
			serializer = self.serializer_class(profile, many=True if isinstance(profile, list) else False)
			return Response({
				"status": "success",
				"status_code": status.HTTP_200_OK,
				"details": "Profie fetched.",
				"data": serializer.data 
			})

		except Exception as e:
			logger.error(f"An error occured when trying to get user profile: {e}", exc_info=True)
			return Response({
				"status":"error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


# profile detail view
class ProfileDetailRequest(APIView):
	permissions_classes = [permissions.IsAuthenticated, ]
	serializer_class = ProfileSerializer

	# get profile object
	async def get_object(self, pk):
		try:
			return await asyncio.to_thread(Profile.objects.get, pk=pk)

		except Profile.DoesNotExist:
			raise Http404("Profile does not exist")

		except Exception as e:
			logger.error(f"An error occurred when trying to query profile object: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred when trying to get profile object."
			})

	# get profile details 
	async def get(self, request, pk):
		try:
			profile = await self.get_object(pk)
			serializer = self.serializer_class(profile)
			return Response({
				"status": "success",
				"status_code": status.HTTP_200_OK,
				"details": "Profie details fetched."
				"data": serializer.data
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to get user profile details: {e}". exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# update profile with PUT method 
	async def put(self, request, pk):
		try:
			profile = await self.get_object(pk)
			serializer = self.serializer_class(profile, data=request.data)

			if serializer.is_valid(raise_exception=True):
				async with database.transaction():
					await asyncio.to_thread(serializer.save(user=self.request.user))

				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "Profile updated."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Unable to update profile details."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to update user profile using the PUT method: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# update profile with PATCH method 
	async def patch(self, request, pk):
		try:
			profile = await self.get_object(pk)
			serializer = self.serializer_class(profile, data=request.data)

			if serializer.is_valid(raise_exception=True):
				async with database.transaction():
					await asyncio.to_thread(serializer.save(user=self.request.user))

				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "Profile updated."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Unable to update profile details."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to update user profile using the PATCH method: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# delete profile
	async def delete(self, request, pk):
		try:
			profile = await self.get_object(pk)
			profile.delete()
			return Response({
				"status": "success",
				"status_code": status.HTTP_204_NO_CONTENT,
				"details": "Profile deleted."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to delete user profile: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later"
			})



# user view 
class UserRequest(APIView):
	permissions_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer

	# user queryset to get user based on the permissions of the user 
	async def get_queryset(self):
		user = self.request.user 
		try:
			if user.is_staff or user.is_superuser:
				return await asyncio.to_thread(User.objects.all)

			user_object = await asyncio.to_thread(User.objects.get, username__iexact=user.username)
			return user_object

		except User.DoesNotExist:
			raise Http404("User does not exist")

		except Exception as e:
			logger.error(f"An error occurred on user queryset: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred in getting user object."
			})


	async def get(self, request):
		try:
			user = await self.get_queryset()
			serializer = self.serializer_class(user, many=True if isinstance(user, list) else False)
			return Response({
				"status": "success",
				"status_code": status.HTTP_200_OK,
				"details": "User fetched.",
				"data": serializer.data 
			})

		except Exception as e:
			logger.error(f"An error occured when trying to get user object: {e}", exc_info=True)
			return Response({
				"status":"error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


# user detail view
class UserDetailRequest(APIView):
	permissions_classes = [permissions.IsAuthenticated, ]
	serializer_class = UserSerializer

	# get user object
	async def get_object(self, pk):
		try:
			return await asyncio.to_thread(User.objects.get, pk=pk)

		except User.DoesNotExist:
			raise Http404("User does not exist")

		except Exception as e:
			logger.error(f"An error occurred when trying to query user object: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred when trying to get user object."
			})

	# get user details 
	async def get(self, request, pk):
		try:
			user = await self.get_object(pk)
			serializer = self.serializer_class(user)
			return Response({
				"status": "success",
				"status_code": status.HTTP_200_OK,
				"details": "User details fetched."
				"data": serializer.data
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to get user details: {e}". exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# update user with PUT method 
	async def put(self, request, pk):
		try:
			user = await self.get_object(pk)
			serializer = self.serializer_class(user, data=request.data, context={'request':request}, partail=True)

			if serializer.is_valid(raise_exception=True):
				async with database.transaction():
					await asyncio.to_thread(serializer.save)

				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "User updated."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Unable to update user details."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to update user using the PUT method: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# update user with PATCH method 
	async def patch(self, request, pk):
		try:
			user = await self.get_object(pk)
			serializer = self.serializer_class(user, data=request.data, context={'request':request})

			if serializer.is_valid(raise_exception=True):
				async with database.transaction():
					await asyncio.to_thread(serializer.save)

				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "User updated."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Unable to update user details."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to update user profile using the PATCH method: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# delete user
	async def delete(self, request, pk):
		try:
			user = self.request.user 

			if user.is_staff or user.is_superuser:
				user = await self.get_object(pk)
				user.delete()
				return Response({
					"status": "success",
					"status_code": status.HTTP_204_NO_CONTENT,
					"details": "User deleted."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_401_UNAUTHORIZED,
				"details": "You are not authorized to delete user account. Please contact support if you want your account deleted."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to delete user account: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later"
			})



# file view 
class FileRequest(APIView):
	permissions_classes = [permissions.IsAuthenticated, ]
	parser_classes = [MultiPartParser, FormParser, ]
	serializer_class = FileSerializer


	# file queryset to get file based on the permissions of the user 
	async def get_queryset(self):
		user = self.request.user 
		try:
			if user.is_staff or user.is_superuser:
				return await asyncio.to_thread(File.objects.all)

			file = await asyncio.to_thread(File.objects.get, user=user)
			return file

		except File.DoesNotExist:
			raise Http404("File does not exist")

		except Exception as e:
			logger.error(f"An error occurred on file queryset: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred in getting user object."
			})

	# get file 
	async def get(self, request):
		try:
			file = await self.get_queryset()
			serializer = self.serializer_class(file, many=True if isinstance(file, list) else False)
			return Response({
				"status": "success",
				"status_code": status.HTTP_200_OK,
				"details": "File fetched.",
				"data": serializer.data 
			})

		except Exception as e:
			logger.error(f"An error occured when trying to get file object: {e}", exc_info=True)
			return Response({
				"status":"error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later."
			})


	# create file 
	async def post(self, request):
		try:
			serializer = self.serializer_class(data=request.data)
			if serializer.is_valid(raise_exception=True):
				async with database.transaction():
					await asyncio.to_thread(serializer.save(user=self.request.user))
				return Response({
					"status": "success",
					"status_code": status.HTTP_201_CREATED,
					"details": "File Uploaded."
				})

			return Response({
				"status": "error",
				"status_code": status.HTTP_400_BAD_REQUEST,
				"details": serializer.errors,
				"error_message": "Unable to upload file"
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to upload file: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later"
			})


# file detail view 
class FileDetailRequest(APIView):

	# get file object
	async def get_object(self, pk):
		try:
			return await asyncio.to_thread(File.objects.get, pk=pk)

		except File.DoesNotExist:
			raise Http404("File does not exist")

		except Exception as e:
			logger.error(f"An error occurred when trying to query file object: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred when trying to get user object."
			})

	# delete file
	async def delete(self, request, pk):
		try:
			file = await self.get_object(pk)
			file.delete()
			return Response({
				"status": "success",
				"status_code": status.HTTP_204_NO_CONTENT,
				"details": "File deleted."
			})

		except Exception as e:
			logger.error(f"An error occurred when trying to delete file: {e}", exc_info=True)
			return Response({
				"status": "error",
				"status_code": HTTP_500_INTERNAL_SERVER_ERROR,
				"details": "An error occurred. Please try again later"
			})

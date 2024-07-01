import asyncio 
import logging 
from django.db.models import Q 
from django.http import Http404
from django.contrib.auth import get_user_model
from rest_framework import status, permissions
from rest_framework.views import APIView 
from rest_framework.response import Response 
from rest_framework.parsers import MultiPartParser, FormParser

from .serializers import ProfileSerializer, FileSerializer, FileOperationSerializer
from fileshare.database import database 

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
					await asyncio.to_thread(serializer.save)

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
					await asyncio.to_thread(serializer.save)

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
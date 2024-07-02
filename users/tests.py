from django.urls import reverse 
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Profile

User = get_user_model()



class UserViewTest(APITestCase):
	"""
	Test get, put, patch and delete method for user view

	"""

	def setUp(self):
		"""
		setup test 

		"""

		# create user 
		self.new_user = User.objects.create_user(username="newuser", email="newuser@email.com", password="newUSER12##")

		# generate token for user 
		refresh = RefreshToken.for_user(self.new_user)
		self.token = str(refresh.access_token)


		# set credentials with token 
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

		# user url, get user detail by primary key 
		self.user_url = reverse("user_details", kwargs={'pk':self.new_user.pk})

		# this data will be used for put method, since the code does not allow partial update when using put method
		self.user_update_data = {
			"username": "newestuser",
			"email":"newestuser@email.com"
		}

		# this will be used for patch method, since it allows patial edit
		self.user_update_data_2 ={
			"username": "latestusername"
		}

	def test_get_user(self):
		"""
		test GET method on user_details view  

		"""
		response = self.client.get(self.user_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn('username', response.data['data'])


	def test_put_user(self):
		"""
		test PUT method on user_details view 

		"""
		response = self.client.put(self.user_url, self.user_update_data, format='json')
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertIn('success', response.data)


	def test_patch_user(self):
		"""
		test PATCH method on user_detail view

		"""
		response = self.client.patch(self.user_url, self.user_update_data_2, format='json')
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_201_CREATED)
		self.assertIn('success', response.data)


	def test_delete_user(self):
		"""
		test DELETE method on user_details view

		"""
		response = self.client.delete(self.user_url)
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_401_UNAUTHORIZED) # only admin or staff can delete user
		self.assertIn('error', response.data)


class ProfileViewTest(APITestCase):
	"""
	test for profile crud operation

	"""

	def setUp(self):
		"""
		setup test

		"""
		# create user 
		self.new_user = User.objects.create_user(username="newuser", email="newuser@email.com", password="newUSER12##")

		# get user profile 
		self.user_profile = self.new_user.user_profile

		# generate token for user 
		refresh = RefreshToken.for_user(self.new_user)
		self.token = str(refresh.access_token)


		# set credentials with token 
		self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

		# user url, get user detail by primary key 
		self.profile_url = reverse("profile_details", kwargs={'pk':self.user_profile.pk})


	def test_get_profile(self):
		"""
		test GET method on profile_details view 

		"""
		response = self.client.get(self.profile_url)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertIn("success", response.data)


	def test_delete_profile(self):
		"""
		test DELETE method on profile_details view 

		"""

		response = self.client.delete(self.profile_url)
		response_status = response.data['status']
		self.assertEqual(response_status, status.HTTP_204_NO_CONTENT)
		self.assertIn('success', response.data)


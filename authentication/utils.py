from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend 
from django.db.models import Q
from rest_framework_simplejwt.utils import jwt_payload_handler 


User = get_user_model()

# add username to jwt payload 
def custom_jwt_payload_handler(user):
	payload = jwt_payload_handler(user)
	payload['username'] = user.username
	return payload 


# custom auth backend  to login with either username or email 
class CustomAuthBackend(ModelBackend):
	def authenticate(self, request, username=None, password=None, **kwargs) -> None:
		try:
			# fetch user by username or email 
			user = User.objects.get(Q(username__iexact=username) | Q(email__iexact=username))

		except User.DoesNotExist:
			return None 

		if user.check_password(password):
			return user 

		return None 
import re 
from django.contrib.auth.password_validation import validate_password 
from django.contrib.auth import get_user_model
from rest_framework import serializers 

User = get_user_model()


# registration serializer
class SignUpSerializer(serializers.ModelSerializer):
	username = serializers.CharField(required=True)
	email = serializers.EmailField(required=True)
	password = serializers.CharField(required=True)
	password_again = serializers.CharField(required=True)

	class Meta:
		model = User 
		fields = ['username', 'email', 'password', 'password_again']

	# validate username 
	def validate_username(self, value):
		errors = {}

		if value is None or not value.strip():
			errors["username_value"] = "Username cannot be empty or filled with white space"

		if len(value) < 4 or len(value) > 20:
			errors["username_length"] = "Username must be between 4 to 20 characters"

		check_username = User.objects.filter(username__iexact=value)

		if check_username.exists():
			errors["username_exists"] = f"Username {value} is not available"

		pattern = r'[!@#$%^&*()+\-={}\[\]:;"\'<>,.?/\\|`~]'

		if re.search(pattern, value):
			errors["username_character"] = "Username cannot contain any special character except '_'"

		value.replace(" ", "_") # replace white space with underscore if there is whitespace in username

		if errors:
			raise serializers.ValidationError(errors)

		return value


	# validate email 
	def validate_email(self, value):
		errors = {}

		if value is None or not value.strip():
			errors["email_value"] = "Email cannot be empty or filled with white space only"

		if len(value) < 6 or len(value) > 40:
			errors["email_length"] = "Email must be between 6 to 40 characters"

		check_email = User.objects.filter(email__iexact=value)

		if check_email.exists():
			errors["email_exists"] = f"Email {value} is not available"

		if errors:
			raise serializers.ValidationError(errors)

		return value 

	# validate passwords 
	def validate(self, data):
		errors = {}
		password = data.get("password")
		password_again = data.get("password_again")

		if password is None or not password.strip():
			errors["password_value"] = "Passwords cannot be empty or filled with white space only"

		if len(password) < 8:
			errors["password_length"] = "Passwords must be at least 8 characters"

		if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
			errors["password_character"] = "Passwords must contain at least one special character"

		if not any(p.isupper() for p in password):
			errors["password_uppercase"] = "Passwords must contain at least one uppercase letter"

		if not any(p.islower() for p in password):
			errors["password_lowercase"] = "Passwords must contain at least one lowercase letter"

		if not any(p.isdigit() for p in password):
			errors["password_digit"] = "Passwords must contain at least one number"

		if password != password_again:
			errors["password_match"] = "Both passwords must match"

		if errors:
			password_error = {"password": [errors]}
			raise serializers.ValidationError(password_error)

		return data 


	# create user 
	def create(self, validated_data):
		username = validated_data["username"]
		email = validated_data["email"]
		password = validated_data["password"]

		user = User.objects.create(
			username=username,
			email=email,
		)
		user.set_password(password)
		user.save()

		return user 



# sign in serializer 
class SignInSerializer(serializers.Serializer):
	login_id = serializers.CharField(max_length=40, required=True)
	password = serializers.CharField(required=True)


# password change serializer
class ChangePasswordSerializer(serializers.Serializer):
	old_password = serializers.CharField(required=True)
	new_password = serializers.CharField(required=True)
	new_password_again = serializers.CharField(required=True)

	# validate data 
	def validate(self, data):
		errors = {}
		user = self.context['request'].user 
		old_password = self.data.get("old_password")
		new_password = self.data.get("new_password")
		new_password_again = self.data.get("new_password_again")

		if not user.check_password(old_password):
			errors["old_password"] = "Old password is not correct"

		if new_password is None or not new_password.strip():
			errors["password_value"] = "Passwords cannot be empty or filled with white space only"

		if len(new_password) < 8:
			errors["password_length"] = "Passwords must be at least 8 characters"

		if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", new_password):
			errors["password_character"] = "Passwords must contain at least one special character"

		if not any(p.isupper() for p in new_password):
			errors["password_uppercase"] = "Passwords must contain at least one uppercase letter"

		if not any(p.islower() for p in new_password):
			errors["password_lowercase"] = "Passwords must contain at least one lowercase letter"

		if not any(p.isdigit() for p in new_password):
			errors["password_digit"] = "Passwords must contain at least one number"

		if new_password != new_password_again:
			errors["password_match"] = "Both passwords must match"

		if errors:
			password_error = {"password": [errors]}
			raise serializers.ValidationError(password_error)

		return data 


		# save data 
		def save(self):
			user = self.context['request'].user 
			user.set_password(self.validated_data["new_password"])
			user.save()
			
			return user 
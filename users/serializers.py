from django.contrib.auth import get_user_model
from rest_framework import serializers 
from.models import Profile, File, FileOperation 


User = get_user_model()


# user serializer 
class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User 
		fields = ['id', 'username', 'email']



	# validate username 
	def validate_username(self, value):
		errors = {}
		user = self.context['request'].user 

		if value is None or not value.strip():
			errors["username_value"] = "Username cannot be empty or filled with white space"

		if len(value) < 4 or len(value) > 20:
			errors["username_length"] = "Username must be between 4 to 20 characters"

		check_username = User.objects.filter(username__iexact=value)

		if value != user.username and check_username.exists():
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
		user = self.context['request'].user

		if value is None or not value.strip():
			errors["email_value"] = "Email cannot be empty or filled with white space only"

		if len(value) < 6 or len(value) > 40:
			errors["email_length"] = "Email must be between 6 to 40 characters"

		check_email = User.objects.filter(email__iexact=value)

		if value != user.email and check_email.exists():
			errors["email_exists"] = f"Email {value} is not available"

		if errors:
			raise serializers.ValidationError(errors)

		return value 


	# save data 
	def save(self):
		user = self.context['request'].user 
		user.username = self.validated_data["username"]
		user.email = self.validated_data["email"]
		user.save()
		
		return user 


# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.CharField(required=False) # this returns string value of user object

	class Meta:
		model = Profile
		fields = ['id', 'fullname', 'user',]


# file serializer
class FileSerializer(serializers.ModelSerializer):
	user = serializers.CharField(required=False) # this returns string value of user object
	file = serializers.FileField(required=True)

	class Meta:
		model = File 
		fields = ['id', 'file', 'user', 'date_uploaded']


# file operation serializer
class FileOperationSerializer(serializers.ModelSerializer):
	file = serializers.CharField(required=False) # this returns string value of file object
	sender = serializers.CharField(required=False) # this returns string value of user object
	receiver = serializers.CharField(required=False) # this returns string value of user object

	class Meta:
		model = File
		fields = ['id', 'file', 'sender', 'receiver', 'date']


	# validate data 
	def validate(self, data):
		errors = {}
		# this gets the file 'id' which is sent with the data  
		file = self.data.get('file')
		receiver = self.data.get('receiver')

		check_receiver = User.objects.get(Q(username__iexact=receiver) | Q(email__iexact=receiver))
		check_file = File.objects.get(id=file)

		if not check_receiver.exists():
			errors["receiver_id"] = f"The receiver id {receiver} does not match any account."

		if not check_file.exists():
			errors["file_id"] = "The file you request does not exist". 

		if errors:
			raise serializers.ValidationError(errors)

		return data 


	# create file operation object 
	def create(self, validated_data):
		user = self.context['request'].user 
		file = self.validated_data['file']
		receiver = self.validated_data['receiver']

		check_receiver = User.objects.get(Q(username__iexact=receiver) | Q(email__iexact=receiver))
		check_file = File.objects.get(id=file)

		file_operation = FileOperation.objects.create(
			file = check_file,
			sender = user,
			receiver = check_receiver 
		)
		file_operation.save()

		return file_operation





from rest_framework import serializers 
from.models import Profile, File, FileOperation 



# Profile serializer
class ProfileSerializer(serializers.ModelSerializer):
	user = serializers.CharField(required=False) # this returns string value of user object

	class Meta:
		model = Profile
		fields = ['id', 'fullname', 'user',]


# file serializer
class FileSerializer(serializers.ModelSerializer):
	user = serializers.CharField(required=False) # this returns string value of user object

	class Meta:
		model = File 
		fields = ['id', 'file', 'user', 'date_uploaded']


# file operation serializer
class FileOperationSerializer(serializers.ModelSerializer):
	file = serializers.CharField(required=False) # this returns string value of file object
	sender = serializers.CharField(required=False) # this returns string value of user object
	reciever = serializers.CharField(required=False) # this returns string value of user object

	class Meta:
		model = File
		fields = ['id', 'file', 'sender', 'reciever', 'operation', 'date']



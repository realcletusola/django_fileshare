from django.db import models
from django.contrib.auth import get_user_model 

User = get_user_model()


# profile model 
class Profile(models.Model):
	fullname = models.CharField(max_length=50, null=True, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
	account_disabled = models.BooleanField(default=False)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.User

	class Meta:
		ordering = ['-date_created']


# file model 
class File(models.Model):
	file = models.FileField(upload_to='documents/', null=False, blank=False)
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_file')
	date_uploaded = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.file

	class Meta:
		ordering = ['-date_uploaded']


# file operation model
class FileOperation(models.Model):

	operation_type = (
		('send','send'),
		('recieved', 'recieved')
	)

	file = models.OneToOneField(File, on_delete=models.CASCADE, related_name='file')
	sender = models.OneToOneField(User, on_delete=models.CASCADE, related_name='file_sender')
	reciever = models.OneToOneField(User, on_delete=models.CASCADE, related_name='file_reciever')
	operation = models.CharField(choices=operation_type, default='send', max_length=15)
	date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.file

	class Meta:
		ordering = ['-date_sent']





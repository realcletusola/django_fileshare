from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.utils import timezone 


# custom user manager class  
class CustomUserManager(UserManager):
	# function to create user
	def create_user(self, username, email, password, **extra_fields):
		if not username:
			raise ValueError("Username is required")

		if not email:
			raise ValueError("Email is required")

		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user 


	# function to create super user 
	def create_superuser(self, username, email, password, **extra_fields):
		extra_fields.setdefault('is_active', True)
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		return self.create_user(username, email, password, **extra_fields)


# custom user model 
class CustomUser(AbstractUser):
	username = models.CharField(max_length=20, unique=True)
	email = models.EmailField(max_length=40, unique=True)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	groups = models.ManyToManyField(Group, blank=True, related_name='user_group')
	permissions = models.ManyToManyField(Permission, blank=True, related_name='user_permission')
	login_trials = models.IntegerField(default=0)  
	max_login_trials = models.IntegerField(default=5)
	last_failed_login = models.DateTimeField(null=True, blank=True)
	time = models.DateTimeField(auto_now_add=True)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELD = ['email']

	objects = CustomUserManager()

	def __str__(self):
		return self.username

	# function to increase login trials on failed login attempt 
	def increment_login_trials(self):
		self.login_trials += 1
		self.last_failed_login = timezone.now()
		self.save()

	# function to reset login trails after successful authentication
	def reset_login_trials(self):
		self.login_trials = 0
		self.last_failed_login = None
		self.save()


	class Meta:
		ordering = ['-time']
		verbose_name = 'CustomUser'
		verbose_name_plural = 'CustomUsers'


from datetime import timezone

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class UserProfileManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifier
    for authentication instead of usernames.
    """
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not password:
            raise ValueError('The Password field must be set')

        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    """ Model using email as the primary authentication field.
    Includes additional fields for user profiles and avatar.
    """
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=255,
        unique=True,
        blank=True,
        null=True,
        help_text="Optional username. Email is used for authentication."
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False,
                                       help_text="Designates that this user has all permissions without explicitly assigning them.")
    is_admin = models.BooleanField(default=False, help_text="Custom field to designate an admin role.")
    date_joined = models.DateTimeField(auto_now_add=True)
    # user may have not have logged in yet, so last login is optional
    last_login = models.DateTimeField(blank=True, null=True)
    # have not done this before. Would need some kind of validation logic and exception handling to make sure the user
    # has actually loaded an avatar image.
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email' # Use email for authentication

    def __str__(self):
        """
        Returns the email as the string representation of the user.
        """
        return self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between, email if no name is preset        """
        full_name = f"{self.first_name} {self.last_name}".strip()
        return full_name or self.email

    def get_username(self):
        """
        Returns the unique identifier for this User, which is the email.
        """
        return self.email
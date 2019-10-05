from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.base import ModelBase
from mynewsite import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

class UserManager(BaseUserManager):
    use_in_migrations = True

    def create(self, email, password, first_name=None, last_name=None):
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['password']
    objects = UserManager()

    def __str__(self):
        return self.email


class AuthToken(ModelBase):
    key = models.CharField()
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

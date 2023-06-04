import django
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Gender(models.TextChoices):
        MALE = 'male', _('male')
        FEMALE = 'female', _('female')
        OTHER = 'other', _('other')

    email = models.EmailField(max_length=254, unique=True,
                              verbose_name='Email', help_text='User email')

    first_name = models.CharField(max_length=254, null=True,
                                  blank=True, verbose_name='First name',
                                  help_text='User first name')

    last_name = models.CharField(max_length=254, null=True,
                                 blank=True, verbose_name='Last name',
                                 help_text='User last name')

    birth_date = models.DateField(default=django.utils.timezone.now,
                                  verbose_name='Birth date',
                                  help_text='User birth date')

    last_login = models.DateTimeField(null=True, blank=True,
                                      verbose_name='Last login',
                                      help_text='User last login date')

    age = models.PositiveIntegerField(null=True, blank=True, verbose_name="User age", help_text="User age")
    gender = models.CharField(
        null=True, blank=True,
        max_length=20,
        choices=Gender.choices,
        verbose_name='User gender',
        help_text='User gender'
    )
    address = models.CharField(null=True, blank=True, max_length=255)
    website = models.CharField(null=True, blank=True, max_length=255)
    user_name = models.CharField(max_length=30, unique=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'user_name'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

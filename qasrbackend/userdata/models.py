import random
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phone_number=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            phone_number=phone_number,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, phone_number=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            phone_number=phone_number,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    phone_number = models.CharField(max_length=11, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    last_login = models.DateTimeField(default=timezone.now)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class ResetPasswordToken(models.Model):
    user = models.ForeignKey('Users', on_delete=models.CASCADE)
    token = models.CharField(max_length=4, unique=True)  # Token length is 4 characters
    created_at = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = self._generate_numeric_token()
        # Validate the token length and ensure it's numeric
        if len(self.token) != 5 or not self.token.isdigit():
            raise ValidationError("Token must be exactly 5 numeric characters.")
        super().save(*args, **kwargs)

    def _generate_numeric_token(self):
        # Generate a random 4-digit numeric token
        return f"{random.randint(10000, 99999)}"

    class Meta:
        db_table = 'reset_password_tokens'


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    username = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = PhoneNumberField(null=True, blank=True)
    item_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField()

    price = models.DecimalField(max_digits=10, decimal_places=2,
                                validators=[MinValueValidator(0.01)], default=0.00)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f'Order by {self.user.username} and phone number: {self.phone_number}'


class OrderHistory(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, related_name='history')
    item_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_history'

    def __str__(self):
        return f'History for Order {self.order.id}'


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True,
                                 related_name='payment', default=0)

    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'payments'

    def __str__(self):
        return f'Payment for Order {self.order.id}'


class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True, blank=True)

    class Meta:
        db_table = 'profiles'

    def __str__(self):
        return f'Profile for {self.user.username}'

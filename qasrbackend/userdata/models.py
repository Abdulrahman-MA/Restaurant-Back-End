import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string


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

    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username=username,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Users(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    phone_number = PhoneNumberField(unique=True)

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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(length=64)
        super().save(*args, **kwargs)


class CartItem(models.Model):
    item_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=2000, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='uploads/cart_items/')
    item_type = models.CharField(max_length=255)

    class Meta:
        db_table = 'cart_items'

    def __str__(self):
        return f'{self.name} - {self.item_type}'


class Order(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='orders')
    cart_item = models.ForeignKey(CartItem, on_delete=models.CASCADE, related_name='orders')
    quantity = models.IntegerField()

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f'Order by {self.user.username} for {self.cart_item.name}'


class OrderHistory(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, related_name='history')
    item_name = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField()

    class Meta:
        db_table = 'order_history'

    def __str__(self):
        return f'History for Order {self.order.id}'


class Payment(models.Model):
    payment = models.OneToOneField(Order, on_delete=models.CASCADE, primary_key=True, related_name='payment_amount')
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'payments'

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.order_history = None

    def __str__(self):
        return f'Payment {self.payment_id} for Order History {self.order_history.order.id}'

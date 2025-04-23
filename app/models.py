from .utils import random_num , uuid_generate
from django.contrib.auth.models import AbstractUser
from django.db import models





class User(AbstractUser):
    phone = models.CharField(max_length=16)
    is_verified = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.IntegerField(default=random_num)
    key = models.UUIDField(default=uuid_generate, unique=True)
    resend_count = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Market(models.Model):
    name = models.CharField(max_length=120)
    logo = models.ImageField(upload_to='logo', null=True, blank=True)
    location_lt = models.FloatField()
    location_lg = models.FloatField()
    description = models.TextField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Category(models.Model):
    name = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product', null=True, blank=True)
    price = models.FloatField()
    discount = models.FloatField()
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Rate(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    anonym = models.BooleanField(default=False)
    message = models.TextField()
    rate = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} by {self.user.username if not self.anonym else 'Anonym user'}"


class UserAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    main = models.BooleanField(default=False)
    lt = models.FloatField()
    lg = models.FloatField()
    street = models.CharField(max_length=120)
    city = models.CharField(max_length=120)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    market = models.ForeignKey(Market, on_delete=models.CASCADE)
    user_address = models.ForeignKey(UserAddress, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name} by {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product.name}, {self.quantity}"






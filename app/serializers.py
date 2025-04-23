from rest_framework.serializers import ModelSerializer
from .models import User, OTP , Market , Product , Rate , UserAddress , Order , Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password", "phone", "is_verified")


class OtpSerializer(ModelSerializer):
    class Meta:
        model = OTP
        fields = ("id", "key", "code")

class MarketSerializer(ModelSerializer):
    class Meta:
        model = Market
        fields = ("id", "name", "logo" , "location_lt", "location_lg", "description")

class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("id", "name", "description", "image", "category", "price", "discount", "market", "available")

class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = ("id", "product", "market", "user", "anonym", "message", "rate")

class UserAddressSerializer(ModelSerializer):
    class Meta:
        model = UserAddress
        fields = ("id", "user", "main", "lt", "lg", "street", "city")


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "product", "user", "market", "user_address")

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "name")
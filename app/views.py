import requests
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import OTP
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes
from django.contrib.auth.hashers import check_password
from .utils import *
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

BOT_TOKEN = '8119158643:AAG9Ea_fWA1OOoxGJKHuxepIsH7DrZb_IQM'
CHAT_ID = '8012138812'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"



def send_telegram_message(text):
    payload = {"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"}
    requests.post(TELEGRAM_API_URL, data=payload)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(["POST"])
def registration(request):
    serializer = UserSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    user = serializer.save()
    new_code = random_num()
    new_key = uuid_generate()
    otp = OTP.objects.create(user=user)

    telegram_text = f"Login code: {new_code}."
    send_telegram_message(telegram_text)

    return Response({"key": otp.key}, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'key': openapi.Schema(type=openapi.TYPE_STRING),
        'code': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(["POST"])
def verify(request):
    otp = OTP.objects.filter(key=request.data["key"]).first()
    if not otp:
        return Response({"error": "OTP kaliti topilmadi"}, status=status.HTTP_400_BAD_REQUEST)
    if otp.code != request.data["code"]:
        return Response({"error": "Noto‘g‘ri OTP kodi"}, status=status.HTTP_400_BAD_REQUEST)

    otp.user.is_verified = True
    otp.user.save()
    OTP.objects.filter(user=otp.user).delete()

    return Response({"message": "Foydalanuvchi muvaffaqiyatli tasdiqlandi"}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={'key': openapi.Schema(type=openapi.TYPE_STRING)},
))
@api_view(['POST'])
def resend(request):
    key = request.data.get('key')
    otp = OTP.objects.filter(key=key).first()
    if not otp:
        return Response({"error": "Key not found"}, status=status.HTTP_400_BAD_REQUEST)
    if timezone.now() < otp.created_at + timedelta(seconds=15):
        return Response({"error": "You can only get a new code after 1 minute."}, status=status.HTTP_400_BAD_REQUEST)
    block = OTP.objects.filter(user=otp.user, created_at__gte=timezone.now() - timedelta(hours=2))
    if block.count() >= 3:
        return Response({"error": "Too many OTP requests. Try again later."}, status=status.HTTP_429_TOO_MANY_REQUESTS)
    OTP.objects.create(user=otp.user)
    send_telegram_message(f"Your new code: {otp.code}")
    return Response({"message": "OTP has been sent", "key": otp.key}, status=status.HTTP_200_OK)


@swagger_auto_schema(method='post', request_body=openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'old': openapi.Schema(type=openapi.TYPE_STRING),
        'new': openapi.Schema(type=openapi.TYPE_STRING),
    }
))
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    old = request.data.get("old")
    new = request.data.get("new")

    if not old or not new:
        return Response({"error": "Eski va yangi parolni kiriting!"}, status=status.HTTP_400_BAD_REQUEST)
    if not check_password(old, user.password):
        return Response({"error": "Eski parol noto‘g‘ri!"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new)
    user.save()

    return Response({"message": "Parol muvaffaqiyatli o'zgartirildi!"}, status=status.HTTP_200_OK)



@swagger_auto_schema(method='post', request_body=MarketSerializer)
@api_view(["POST"])
def market_create(request):
    serializer = MarketSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@swagger_auto_schema(method='post', request_body=ProductSerializer)
@api_view(["POST"])
def product_create(request):
    serializer = ProductSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(["POST"])
@permission_classes([IsAuthenticated])
def rate_create(request):
    data = request.data
    try:
        product = Product.objects.get(pk=data["product"])
        market = Market.objects.get(pk=data["market"])
    except (Product.DoesNotExist, Market.DoesNotExist):
        return Response({"error": "Mahsulot yoki market topilmadi."}, status=status.HTTP_404_NOT_FOUND)

    rate = Rate.objects.create(
        product=product,
        market=market,
        user=request.user,
        anonym=data.get("anonym", False),
        message=data.get("message", ""),
        rate=data.get("rate", 0)
    )

    serializer = RateSerializer(rate)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_address_create(request):
    data = request.data.copy()
    data["user"] = request.user.id

    serializer = UserAddressSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def order_create(request):
    data = request.data.copy()
    data["user"] = request.user.id

    serializer = OrderSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
# @api_view(["DELETE"])
# def market_delete(request, pk):
#     market = get_object_or_404(Market, pk=pk)
#     market.delete()
#     return Response({"detail": "Market deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(["DELETE"])
# def product_delete(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     product.delete()
#     return Response({"detail": "Product deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(["DELETE"])
# def rate_delete(request, pk):
#     rate = get_object_or_404(Rate, pk=pk, user=request.user)
#     rate.delete()
#     return Response({"detail": "Rate deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(["DELETE"])
# def user_address_delete(request, pk):
#     address = get_object_or_404(UserAddress, pk=pk)
#     address.delete()
#     return Response({"detail": "Address deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
#
#
# @api_view(["DELETE"])
# def order_delete(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     order.delete()
#     return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
# @api_view(["DELETE"])
# def category_delete(request, pk):
#     order = get_object_or_404(Order, pk=pk)
#     order.delete()
#     return Response({"detail": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
#
#
#

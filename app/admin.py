from django.contrib import admin
from .models import User, OTP, Market, Product, Rate, UserAddress, Order, OrderItem, Category


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'phone', 'is_verified', 'created_at', 'updated_at')
    list_filter = ('is_verified', 'created_at')
    search_fields = ('username', 'phone')
    ordering = ('-created_at',)


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'key', 'resend_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'code')
    ordering = ('-created_at',)
    readonly_fields = ('key',)


@admin.register(Market)
class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'user_id', 'location_lt', 'location_lg', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'user_id__username')
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('market', 'name', 'category', 'price', 'discount', 'available', 'created_at')
    list_filter = ('market', 'category', 'available', 'discount', 'created_at')
    search_fields = ('name', 'market__name', 'category__name')
    ordering = ('-created_at',)


@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ('product', 'market', 'user', 'anonym', 'rate', 'created_at')
    list_filter = ('market', 'product', 'anonym', 'rate')
    search_fields = ('product__name', 'user__username', 'market__name')
    ordering = ('-created_at',)


@admin.register(UserAddress)
class UserAddressAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'street', 'main', 'created_at')
    list_filter = ('city', 'main', 'created_at')
    search_fields = ('user__username', 'city', 'street')
    ordering = ('-created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'market', 'user_address', 'created_at')
    list_filter = ('market', 'created_at')
    search_fields = ('product__name', 'user__username', 'market__name')
    ordering = ('-created_at',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'order__user__username')
    ordering = ('-created_at',)

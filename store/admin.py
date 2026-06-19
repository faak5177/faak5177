from django.contrib import admin
from store.models import Role, User, Category, Manufacturer, Supplier, Product, PickPoint, Order

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'login', 'role')
    list_filter = ('role',)
    search_fields = ('last_name', 'first_name', 'login')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('article', 'name', 'category', 'manufacturer', 'price', 'discount', 'quantity')
    list_filter = ('category', 'manufacturer', 'supplier')
    search_fields = ('article', 'name', 'description')

@admin.register(PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'zip_code', 'city', 'street', 'house')
    search_fields = ('city', 'street')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'status', 'order_date')
    list_filter = ('status',)
    search_fields = ('user__last_name', 'product__name')

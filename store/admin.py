from django.contrib import admin
from store.models import Role, User, Category, Manufacturer, Supplier, Product, PickPoint

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')

@admin.register(User)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'login', 'role')
    list_filter = ('role',)
    search_fields = ('last_name', 'first_name', 'login')

    @admin.display(description='ФИО')
    def full_name(self, obj):
        return obj.full_name

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Manufacturer)
class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'article', 'price', 'discount', 'quantity', 'category')
    list_filter = ('category', 'manufacturer', 'supplier')
    search_fields = ('name', 'article', 'description')

@admin.register(PickPoint)
class PickPointAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'street', 'house', 'zip_code')
    search_fields = ('city', 'street')

from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=100, db_column='Name')
    class Meta:
        db_table = 'Roles'
        managed = False
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
    def __str__(self): return self.name

class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    last_name = models.CharField(max_length=100, db_column='Last_Name')
    first_name = models.CharField(max_length=100, db_column='First_Name')
    middle_name = models.CharField(max_length=100, db_column='Middle_Name')
    login = models.CharField(max_length=200, unique=True, db_column='Login')
    password = models.CharField(max_length=100, db_column='Password')
    role = models.ForeignKey(Role, on_delete=models.CASCADE, db_column='Role_ID')
    class Meta:
        db_table = 'Users'
        managed = False
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    @property
    def full_name(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()
    def __str__(self): return self.full_name

class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')
    class Meta:
        db_table = 'Category'
        managed = False
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
    def __str__(self): return self.name

class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')
    class Meta:
        db_table = 'Manufactures'
        managed = False
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
    def __str__(self): return self.name

class Supplier(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')
    class Meta:
        db_table = 'Suplyers'
        managed = False
        verbose_name = 'Поставщик'
        verbose_name_plural = 'Поставщики'
    def __str__(self): return self.name

class Product(models.Model):
    article = models.CharField(max_length=50, primary_key=True, db_column='Article')
    name = models.CharField(max_length=200, db_column='Name')
    number_measure = models.CharField(max_length=50, db_column='number_measure')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, db_column='Supplier_ID')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, db_column='Manufacturer_ID')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, db_column='Category_ID')
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='Discount')
    quantity = models.IntegerField(default=0, db_column='Quantity')
    description = models.TextField(blank=True, default='', db_column='Description')
    photo = models.CharField(max_length=200, blank=True, default='', db_column='Photo')
    class Meta:
        db_table = 'Products'
        managed = False
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
    @property
    def final_price(self):
        return float(self.price) * (1 - float(self.discount) / 100)
    def __str__(self): return f'{self.article} {self.name}'

class PickPoint(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    zip_code = models.CharField(max_length=20, db_column='Zip_Code')
    city = models.CharField(max_length=100, db_column='City')
    street = models.CharField(max_length=200, db_column='Street')
    house = models.CharField(max_length=20, blank=True, default='', db_column='House')
    class Meta:
        db_table = 'Pickups'
        managed = False
        verbose_name = 'Точка подбора'
        verbose_name_plural = 'Точки подбора'
    def __str__(self): return f'{self.zip_code}, {self.city}, {self.street}, {self.house}'

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменён'),
    ]
    id = models.AutoField(primary_key=True, db_column='ID')
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='User_ID')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='Product_ID', to_field='article')
    quantity = models.IntegerField(db_column='Quantity')
    order_date = models.DateTimeField(auto_now_add=True, db_column='Order_Date')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', db_column='Status')
    pickup_address = models.CharField(max_length=500, blank=True, default='', db_column='Pickup_Address')
    delivery_date = models.DateTimeField(null=True, blank=True, db_column='Delivery_Date')
    class Meta:
        db_table = 'Orders'
        managed = False
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-order_date']
    def __str__(self): return f'Заказ #{self.id}'

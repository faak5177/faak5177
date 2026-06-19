from django.db import models

class Role(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=100, db_column='Name')

    class Meta:
        db_table = 'Roles'
        managed = False

    def __str__(self):
        return self.name

class User(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    last_name = models.CharField(max_length=100, db_column='Last_Name')
    first_name = models.CharField(max_length=100, db_column='First_Name')
    middle_name = models.CharField(max_length=100, db_column='Middle_Name')
    login = models.CharField(max_length=200, db_column='Login', unique=True)
    password = models.CharField(max_length=100, db_column='Password')
    role = models.ForeignKey(
        Role,
        on_delete=models.DO_NOTHING,
        db_column='Role_ID',
        related_name='users'
    )

    class Meta:
        db_table = 'Users'
        managed = False

    @property
    def full_name(self):
        return f"{self.last_name} {self.first_name} {self.middle_name}"

    def __str__(self):
        return self.full_name

class Category(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')

    class Meta:
        db_table = 'Category'
        managed = False

    def __str__(self):
        return self.name

class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')

    class Meta:
        db_table = 'Manufactures'
        managed = False

    def __str__(self):
        return self.name

class Supplier(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    name = models.CharField(max_length=200, db_column='Name')

    class Meta:
        db_table = 'Suplyers'
        managed = False

    def __str__(self):
        return self.name

class Product(models.Model):
    article = models.CharField(max_length=50, db_column='Article', primary_key=True, unique=True)
    name = models.CharField(max_length=200, db_column='Name')
    number_measure = models.CharField(max_length=50, db_column='number_measure')
    price = models.DecimalField(max_digits=10, decimal_places=2, db_column='Price')
    supplier = models.ForeignKey(
        Supplier,
        on_delete=models.DO_NOTHING,
        db_column='Supplier_ID',
        related_name='products'
    )
    manufacturer = models.ForeignKey(
        Manufacturer,
        on_delete=models.DO_NOTHING,
        db_column='Manufacturer_ID',
        related_name='products'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.DO_NOTHING,
        db_column='Category_ID',
        related_name='products'
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, db_column='Discount')
    quantity = models.IntegerField(default=0, db_column='Quantity')
    description = models.TextField(blank=True, db_column='Description')
    photo = models.CharField(max_length=200, blank=True, db_column='Photo')

    class Meta:
        db_table = 'Products'
        managed = False

    @property
    def final_price(self):
        if self.discount and self.discount > 0:
            return self.price * (1 - self.discount / 100)
        return self.price

    @property
    def has_discount(self):
        return self.discount > 0

    def __str__(self):
        return self.name

class PickPoint(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    zip_code = models.CharField(max_length=20, db_column='Zip_Code')
    city = models.CharField(max_length=100, db_column='City')
    street = models.CharField(max_length=200, db_column='Street')
    house = models.CharField(max_length=20, blank=True, db_column='House')

    class Meta:
        db_table = 'Pickups'
        managed = False

    def __str__(self):
        return f"{self.city}, {self.street} ул., д. {self.house}"

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
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_column='User_ID',
        related_name='orders'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        db_column='Product_ID',
        related_name='orders'
    )
    quantity = models.IntegerField(db_column='Quantity')
    order_date = models.DateTimeField(db_column='Order_Date', auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='new',
        db_column='Status'
    )
    pickup_address = models.CharField(
        max_length=500,
        blank=True,
        db_column='Pickup_Address'
    )
    delivery_date = models.DateTimeField(
        null=True,
        blank=True,
        db_column='Delivery_Date'
    )

    class Meta:
        db_table = 'Orders'
        managed = False

    def __str__(self):
        return f"Заказ #{self.id} — {self.product.name}"

from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Создаёт все таблицы (Roles, Users, Category, Manufactures, Suplyers, Products, Pickups, Orders).'
    def handle(self, *args, **opts):
        ddl = [
            'CREATE TABLE IF NOT EXISTS "Roles" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(100) NOT NULL)',
            'CREATE TABLE IF NOT EXISTS "Users" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Last_Name" VARCHAR(100) NOT NULL, "First_Name" VARCHAR(100) NOT NULL, "Middle_Name" VARCHAR(100) NOT NULL, "Login" VARCHAR(200) NOT NULL UNIQUE, "Password" VARCHAR(100) NOT NULL, "Role_ID" INTEGER NOT NULL REFERENCES "Roles"("ID"))',
            'CREATE TABLE IF NOT EXISTS "Category" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL)',
            'CREATE TABLE IF NOT EXISTS "Manufactures" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL)',
            'CREATE TABLE IF NOT EXISTS "Suplyers" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL)',
            'CREATE TABLE IF NOT EXISTS "Products" ("Article" VARCHAR(50) PRIMARY KEY, "Name" VARCHAR(200) NOT NULL, "number_measure" VARCHAR(50) NOT NULL, "Price" DECIMAL(10,2) NOT NULL CHECK ("Price" >= 0), "Supplier_ID" INTEGER NOT NULL REFERENCES "Suplyers"("ID"), "Manufacturer_ID" INTEGER NOT NULL REFERENCES "Manufactures"("ID"), "Category_ID" INTEGER NOT NULL REFERENCES "Category"("ID"), "Discount" DECIMAL(5,2) NOT NULL DEFAULT 0 CHECK ("Discount" >= 0 AND "Discount" <= 100), "Quantity" INTEGER NOT NULL DEFAULT 0 CHECK ("Quantity" >= 0), "Description" TEXT DEFAULT \'\', "Photo" VARCHAR(200) DEFAULT \'\')',
            'CREATE TABLE IF NOT EXISTS "Pickups" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Zip_Code" VARCHAR(20) NOT NULL, "City" VARCHAR(100) NOT NULL, "Street" VARCHAR(200) NOT NULL, "House" VARCHAR(20) DEFAULT \'\')',
            'CREATE TABLE IF NOT EXISTS "Orders" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "User_ID" INTEGER NOT NULL REFERENCES "Users"("ID") ON DELETE CASCADE, "Product_ID" VARCHAR(50) NOT NULL REFERENCES "Products"("Article") ON DELETE CASCADE, "Quantity" INTEGER NOT NULL, "Order_Date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "Status" VARCHAR(20) NOT NULL DEFAULT \'new\', "Pickup_Address" VARCHAR(500) NOT NULL DEFAULT \'\', "Delivery_Date" TIMESTAMP NULL)',
        ]
        with connection.cursor() as c:
            c.execute('PRAGMA foreign_keys = ON')
            for s in ddl: c.execute(s)
        self.stdout.write(self.style.SUCCESS('Таблицы созданы.'))

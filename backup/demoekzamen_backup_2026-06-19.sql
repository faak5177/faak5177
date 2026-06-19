BEGIN TRANSACTION;
CREATE TABLE "Category" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL);
INSERT INTO "Category" VALUES(1,'Общестроительные материалы');
INSERT INTO "Category" VALUES(2,'Стеновые и фасадные материалы');
INSERT INTO "Category" VALUES(3,'Сухие строительные смеси и гидроизоляция');
INSERT INTO "Category" VALUES(4,'Ручной инструмент');
INSERT INTO "Category" VALUES(5,'Защита лица, глаз, головы');
CREATE TABLE "Manufactures" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL);
INSERT INTO "Manufactures" VALUES(1,'М500');
INSERT INTO "Manufactures" VALUES(2,'Изостронг');
INSERT INTO "Manufactures" VALUES(3,'Knauf');
INSERT INTO "Manufactures" VALUES(4,'MixMaster');
INSERT INTO "Manufactures" VALUES(5,'ЛСР');
INSERT INTO "Manufactures" VALUES(6,'ВОЛМА');
INSERT INTO "Manufactures" VALUES(7,'Vinylon');
INSERT INTO "Manufactures" VALUES(8,'Павловский завод');
INSERT INTO "Manufactures" VALUES(9,'Weber');
INSERT INTO "Manufactures" VALUES(10,'Hesler');
INSERT INTO "Manufactures" VALUES(11,'Armero');
INSERT INTO "Manufactures" VALUES(12,'Wenzo Roma');
INSERT INTO "Manufactures" VALUES(13,'KILIMGRIN');
INSERT INTO "Manufactures" VALUES(14,'Исток');
INSERT INTO "Manufactures" VALUES(15,'RUIZ');
INSERT INTO "Manufactures" VALUES(16,'Husqvarna');
INSERT INTO "Manufactures" VALUES(17,'Delta');
CREATE TABLE "Orders" (
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "User_ID" INTEGER NOT NULL REFERENCES "Users"("ID") ON DELETE CASCADE,
        "Product_ID" VARCHAR(50) NOT NULL REFERENCES "Products"("Article") ON DELETE CASCADE,
        "Quantity" INTEGER NOT NULL,
        "Order_Date" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        "Status" VARCHAR(20) NOT NULL DEFAULT 'new',
        "Pickup_Address" VARCHAR(500) NOT NULL DEFAULT '',
        "Delivery_Date" TIMESTAMP NULL);
CREATE TABLE "Pickups" (
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Zip_Code" VARCHAR(20) NOT NULL,
        "City" VARCHAR(100) NOT NULL,
        "Street" VARCHAR(200) NOT NULL,
        "House" VARCHAR(20) DEFAULT '');
CREATE TABLE "Products" (
        "Article" VARCHAR(50) PRIMARY KEY,
        "Name" VARCHAR(200) NOT NULL,
        "number_measure" VARCHAR(50) NOT NULL,
        "Price" DECIMAL(10,2) NOT NULL,
        "Supplier_ID" INTEGER NOT NULL REFERENCES "Suplyers"("ID"),
        "Manufacturer_ID" INTEGER NOT NULL REFERENCES "Manufactures"("ID"),
        "Category_ID" INTEGER NOT NULL REFERENCES "Category"("ID"),
        "Discount" DECIMAL(5,2) NOT NULL DEFAULT 0,
        "Quantity" INTEGER NOT NULL DEFAULT 0,
        "Description" TEXT DEFAULT '',
        "Photo" VARCHAR(200) DEFAULT '');
CREATE TABLE "Roles" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(100) NOT NULL);
INSERT INTO "Roles" VALUES(1,'Администратор');
INSERT INTO "Roles" VALUES(2,'Менеджер');
INSERT INTO "Roles" VALUES(3,'Авторизированный клиент');
CREATE TABLE "Suplyers" ("ID" INTEGER PRIMARY KEY AUTOINCREMENT, "Name" VARCHAR(200) NOT NULL);
CREATE TABLE "Users" (
        "ID" INTEGER PRIMARY KEY AUTOINCREMENT,
        "Last_Name" VARCHAR(100) NOT NULL,
        "First_Name" VARCHAR(100) NOT NULL,
        "Middle_Name" VARCHAR(100) NOT NULL,
        "Login" VARCHAR(200) NOT NULL UNIQUE,
        "Password" VARCHAR(100) NOT NULL,
        "Role_ID" INTEGER NOT NULL REFERENCES "Roles"("ID"));
COMMIT;

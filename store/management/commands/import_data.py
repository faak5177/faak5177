import csv, os
from django.core.management.base import BaseCommand
from store.models import Role, User, Category, Manufacturer, Supplier, Product, PickPoint

class Command(BaseCommand):
    help = 'Import data from CSV files'
    def handle(self, *args, **opts):
        base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
        def csv_iter(name):
            path = os.path.join(base, name)
            with open(path, encoding='utf-8-sig') as f:
                return list(csv.DictReader(f, delimiter=';'))

        Role.objects.all().delete()
        for r in csv_iter('Роли.csv'):
            Role.objects.create(id=int(r['ID']), name=r['Name'])

        User.objects.all().delete()
        for r in csv_iter('Пользователи.csv'):
            User.objects.create(id=int(r['ID']),
                last_name=r['Last_Name'], first_name=r['First_Name'], middle_name=r['Middle_Name'],
                login=r['Login'], password=r['Password'], role_id=int(r['Role_ID']))

        Category.objects.all().delete()
        for r in csv_iter('Категории.csv'):
            Category.objects.create(id=int(r['ID']), name=r['Name'])

        Manufacturer.objects.all().delete()
        for r in csv_iter('Производители.csv'):
            Manufacturer.objects.create(id=int(r['ID']), name=r['Name'])

        Supplier.objects.all().delete()
        for r in csv_iter('Поставщики.csv'):
            Supplier.objects.create(id=int(r['ID']), name=r['Name'])

        Product.objects.all().delete()
        for r in csv_iter('Товары.csv'):
            Product.objects.create(
                article=r['Article'], name=r['Name'], number_measure=r['number_measure'],
                price=r['Price'], supplier_id=int(r['Supplier_ID']),
                manufacturer_id=int(r['Manufacturer_ID']), category_id=int(r['Category_ID']),
                discount=r['Discount'], quantity=int(r['Quantity']),
                description=r['Description'] or '', photo=r['Photo'] or '')

        PickPoint.objects.all().delete()
        for r in csv_iter('Точки подбора.csv'):
            PickPoint.objects.create(zip_code=r['Zip_Code'], city=r['City'],
                street=r['Street'], house=r['House'] or '')

        self.stdout.write(self.style.SUCCESS(
            f'Импорт: Roles={Role.objects.count()}, Users={User.objects.count()}, '
            f'Category={Category.objects.count()}, Manufactures={Manufacturer.objects.count()}, '
            f'Suplyers={Supplier.objects.count()}, Products={Product.objects.count()}, '
            f'Pickups={PickPoint.objects.count()}'))

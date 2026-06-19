from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
from PIL import Image
import os
import uuid

from demoekz_project.settings import BASE_DIR, STATICFILES_DIRS
from store.models import (
    Product, User as StoreUser, Order,
    Category, Manufacturer, Supplier
)

UPLOAD_DIR = os.path.join(STATICFILES_DIRS[0], 'uploads')

def get_store_user(request):
    """Получить StoreUser из Django Auth User."""
    if request.user.is_authenticated:
        try:
            return StoreUser.objects.get(login=request.user.username)
        except StoreUser.DoesNotExist:
            return None
    return None

def get_user_display(request):
    """Отображаемое имя пользователя или 'Гость'."""
    su = get_store_user(request)
    if su:
        return su.full_name
    if request.user.is_authenticated:
        return request.user.get_full_name() or request.user.username
    return 'Гость'

def _resize_photo(uploaded_file):
    """Сохраняет фото в UPLOAD_DIR, масштабируя до 300x200. Возвращает имя файла."""
    os.makedirs(UPLOAD_DIR, exist_ok=True)
    ext = os.path.splitext(uploaded_file.name)[1].lower() or '.jpg'
    filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)

    img = Image.open(uploaded_file)
    img = img.convert('RGB')
    img = img.resize((300, 200), Image.LANCZOS)
    fmt = 'JPEG' if ext in ('.jpg', '.jpeg') else 'PNG'
    img.save(filepath, fmt, quality=85)
    return filename

def _delete_photo_file(photo_name):
    if photo_name:
        path = os.path.join(UPLOAD_DIR, photo_name)
        if os.path.isfile(path):
            os.remove(path)

def _next_article():
    max_num = 0
    for art in Product.objects.values_list('article', flat=True):
        try:
            max_num = max(max_num, int(art))
        except (ValueError, TypeError):
            continue
    return str(max_num + 1)

def login_view(request):
    if request.method == 'POST':
        login_value = request.POST.get('login', '').strip()
        password_value = request.POST.get('password', '').strip()

        if not login_value or not password_value:
            messages.error(request, 'Заполните оба поля: логин и пароль.')
        else:
            auth_user = authenticate(request, username=login_value, password=password_value)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('product_list')
            else:
                messages.error(request, 'Неверный логин или пароль.')
    return render(request, 'store/login.html', {'user_display': 'Гость'})

def logout_view(request):
    logout(request)
    if request.session.session_key:
        request.session.delete()
    return redirect('login')

def product_list(request):
    store_user = get_store_user(request)
    role_id = store_user.role_id if store_user else 0
    search = request.GET.get('search', '').strip()
    sort_by = request.GET.get('sort', 'name')
    category_filter = request.GET.get('category', '')
    manufacturer_filter = request.GET.get('manufacturer', '')
    products = Product.objects.all().select_related('category', 'manufacturer', 'supplier')
    if search:
        products = products.filter(
            Q(name__icontains=search) | Q(article__icontains=search) |
            Q(description__icontains=search) | Q(number_measure__icontains=search) |
            Q(category__name__icontains=search) | Q(manufacturer__name__icontains=search) |
            Q(supplier__name__icontains=search)
        )
    if category_filter:
        products = products.filter(category_id=category_filter)
    if manufacturer_filter:
        products = products.filter(manufacturer_id=manufacturer_filter)
    sort_fields = {'name': 'name', 'price_asc': 'price', 'price_desc': '-price',
        'discount_asc': 'discount', 'discount_desc': '-discount',
        'quantity_asc': 'quantity', 'quantity_desc': '-quantity'}
    products = products.order_by(sort_fields.get(sort_by, 'name'))
    can_manage = role_id in (1, 2)
    can_admin = role_id == 1
    categories = Category.objects.all().order_by('name') if can_manage else None
    manufacturers = Manufacturer.objects.all().order_by('name') if can_manage else None
    return render(request, 'store/product_list.html', {
        'products': products, 'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': role_id,
        'can_manage': can_manage, 'can_admin': can_admin,
        'categories': categories, 'manufacturers': manufacturers,
        'current_search': search, 'current_sort': sort_by,
        'current_category': category_filter, 'current_manufacturer': manufacturer_filter,
    })

def product_create(request):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    saved = False
    if request.method == 'POST':
        article = request.POST.get('article', '').strip()
        name = request.POST.get('name', '').strip()
        price_raw = request.POST.get('price', '')
        photo_file = request.FILES.get('photo')
        try:
            if not article: raise ValueError('Артикул не может быть пустым.')
            if Product.objects.filter(article=article).exists():
                raise ValueError(f'Товар с артикулом «{article}» уже есть.')
            if not name: raise ValueError('Наименование пусто.')
            try: price = float(price_raw) if price_raw else 0.0
            except ValueError: raise ValueError('Цена должна быть числом.')
            if price < 0: raise ValueError('Цена не может быть отрицательной.')
            photo_name = _resize_photo(photo_file) if photo_file else ''
            Product.objects.create(
                article=article, name=name,
                number_measure=request.POST.get('number_measure', 'шт'),
                price=price,
                supplier_id=int(request.POST.get('supplier_id')),
                manufacturer_id=int(request.POST.get('manufacturer_id')),
                category_id=int(request.POST.get('category_id')),
                discount=float(request.POST.get('discount') or 0),
                quantity=int(request.POST.get('quantity') or 0),
                description=request.POST.get('description', '').strip(),
                photo=photo_name)
            messages.success(request, f'Товар «{name}» добавлен.')
            saved = True
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'store/product_form.html', {
        'categories': Category.objects.all().order_by('name'),
        'manufacturers': Manufacturer.objects.all().order_by('name'),
        'suppliers': Supplier.objects.all().order_by('name'),
        'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': store_user.role_id,
        'action': 'Добавление', 'next_article': _next_article(), 'saved': saved})

def product_edit(request, article):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    product = get_object_or_404(Product, article=article)
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        price_raw = request.POST.get('price', '')
        photo_file = request.FILES.get('photo')
        try:
            if not name: raise ValueError('Наименование пусто.')
            try: price = float(price_raw) if price_raw else 0.0
            except ValueError: raise ValueError('Цена должна быть числом.')
            if price < 0: raise ValueError('Цена отрицательная.')
            discount = float(request.POST.get('discount') or 0)
            if discount < 0: raise ValueError('Скидка отрицательная.')
            quantity = int(request.POST.get('quantity') or 0)
            if quantity < 0: raise ValueError('Кол-во отрицательное.')
            if photo_file:
                _delete_photo_file(product.photo)
                product.photo = _resize_photo(photo_file)
            product.name = name
            product.number_measure = request.POST.get('number_measure', 'шт')
            product.price = price
            product.supplier_id = int(request.POST.get('supplier_id'))
            product.manufacturer_id = int(request.POST.get('manufacturer_id'))
            product.category_id = int(request.POST.get('category_id'))
            product.discount = discount
            product.quantity = quantity
            product.description = request.POST.get('description', '').strip()
            product.save()
            messages.success(request, f'Товар «{name}» обновлён.')
        except ValueError as e:
            messages.error(request, str(e))
    return render(request, 'store/product_form.html', {
        'product': product,
        'categories': Category.objects.all().order_by('name'),
        'manufacturers': Manufacturer.objects.all().order_by('name'),
        'suppliers': Supplier.objects.all().order_by('name'),
        'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': store_user.role_id,
        'action': 'Редактирование'})

def product_delete(request, article):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    product = get_object_or_404(Product, article=article)
    if Order.objects.filter(product=product).exists():
        messages.warning(request, f'Нельзя удалить «{product.name}»: в заказах.')
        return redirect('product_list')
    _delete_photo_file(product.photo)
    product.delete()
    messages.success(request, f'Товар {article} удалён.')
    return redirect('product_list')

def order_list(request):
    store_user = get_store_user(request)
    if not store_user: return redirect('login')
    role_id = store_user.role_id
    if role_id not in (1, 2):
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    if role_id == 1:
        orders = Order.objects.all().select_related('user', 'product').order_by('-order_date')
    else:
        orders = Order.objects.filter(user=store_user).select_related('user', 'product').order_by('-order_date')
    return render(request, 'store/order_list.html', {
        'orders': orders, 'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': role_id,
        'can_admin': role_id == 1})

def order_create(request):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    if request.method == 'POST':
        try:
            client = StoreUser.objects.get(id=int(request.POST.get('client_id')))
            product = Product.objects.get(article=request.POST.get('product_article'))
            qty = int(request.POST.get('quantity') or 1)
            if qty <= 0: raise ValueError('Кол-во > 0.')
            delivery_date = None
            d = request.POST.get('delivery_date', '').strip()
            if d:
                from datetime import datetime
                delivery_date = datetime.fromisoformat(d)
            Order.objects.create(user=client, product=product, quantity=qty,
                status=request.POST.get('status', 'new'),
                pickup_address=request.POST.get('pickup_address', '').strip(),
                delivery_date=delivery_date)
            messages.success(request, 'Заказ создан.')
            return redirect('order_list')
        except (ValueError, Product.DoesNotExist, StoreUser.DoesNotExist) as e:
            messages.error(request, str(e) or 'Ошибка.')
    return render(request, 'store/order_create.html', {
        'products': Product.objects.all().order_by('name'),
        'users': StoreUser.objects.all().order_by('last_name'),
        'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': store_user.role_id})

def order_edit(request, order_id):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        try:
            order.product = Product.objects.get(article=request.POST.get('product_article'))
            order.user = StoreUser.objects.get(id=int(request.POST.get('client_id')))
            order.quantity = int(request.POST.get('quantity'))
            order.status = request.POST.get('status', order.status)
            order.pickup_address = request.POST.get('pickup_address', '').strip()
            d = request.POST.get('delivery_date', '').strip()
            if d:
                from datetime import datetime
                order.delivery_date = datetime.fromisoformat(d)
            order.save()
            messages.success(request, 'Заказ обновлён.')
            return redirect('order_list')
        except (ValueError, Product.DoesNotExist, StoreUser.DoesNotExist) as e:
            messages.error(request, str(e) or 'Ошибка.')
    return render(request, 'store/order_edit.html', {
        'order': order,
        'products': Product.objects.all().order_by('name'),
        'users': StoreUser.objects.all().order_by('last_name'),
        'status_choices': Order.STATUS_CHOICES,
        'user_display': get_user_display(request),
        'store_user': store_user, 'role_id': store_user.role_id})

def order_delete(request, order_id):
    store_user = get_store_user(request)
    if not store_user or store_user.role_id != 1:
        messages.error(request, 'Доступ запрещён.')
        return redirect('product_list')
    get_object_or_404(Order, id=order_id).delete()
    messages.success(request, 'Заказ удалён.')
    return redirect('order_list')

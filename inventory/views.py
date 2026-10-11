
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import (
    Q, Sum, F, Count, DecimalField, ExpressionWrapper
)

from .models import Product
from .forms import ProductForm


@login_required
def dashboard(request):
    products = Product.objects.all()

    low_stock = products.filter(
        quantity__gt=0,
        quantity__lte=F('reorder_level')
    )

    inventory_value = products.aggregate(
        total=Sum(
            ExpressionWrapper(
                F('quantity') * F('price'),
                output_field=DecimalField()
            )
        )
    )['total'] or 0

    # Products grouped by category
    category_data = list(
        products.values('category')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )

    # Calculate each stock status
    out_of_stock_count = products.filter(quantity=0).count()

    low_stock_count = low_stock.count()

    in_stock_count = products.filter(
        quantity__gt=F('reorder_level')
    ).count()

    stock_status_data = [
        {'label': 'In Stock', 'total': in_stock_count},
        {'label': 'Low Stock', 'total': low_stock_count},
        {'label': 'Out of Stock', 'total': out_of_stock_count},
    ]

    # Five products with the highest quantity
    top_products = list(
        products.order_by('-quantity', 'name')[:5]
        .values('name', 'quantity')
    )

    context = {
        'total_products': products.count(),
        'low_stock_count': low_stock_count,
        'out_of_stock': out_of_stock_count,
        'inventory_value': inventory_value,
        'recent_products': products.order_by('-id')[:5],
        'low_stock_products': low_stock[:5],

        # Data used by the charts
        'category_data': category_data,
        'stock_status_data': stock_status_data,
        'top_products': top_products,
    }

    return render(request, 'inventory/dashboard.html', context)


@login_required
def product_list(request):
    products = Product.objects.all()

    query = request.GET.get('q', '').strip()
    category = request.GET.get('category', '').strip()

    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(sku__icontains=query)
            | Q(category__icontains=query)
        )

    if category:
        products = products.filter(category=category)

    categories = Product.objects.values_list(
        'category', flat=True
    ).distinct().order_by('category')

    return render(request, 'inventory/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category,
    })


@login_required
def product_add(request):
    form = ProductForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'title': 'Add Product',
    })


@login_required
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)

    form = ProductForm(
        request.POST or None,
        instance=product
    )

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('product_list')

    return render(request, 'inventory/product_form.html', {
        'form': form,
        'title': 'Edit Product',
    })


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('product_list')

    return render(
        request,
        'inventory/product_confirm_delete.html',
        {'product': product}
    )

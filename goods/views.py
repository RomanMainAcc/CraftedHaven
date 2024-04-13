from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products
from goods.utils import q_search


def catalog(request, category_slug=None):
    page_number = request.GET.get('page_number', 1)
    on_sale = request.GET.get('on_sale', None)
    order_by = request.GET.get('order_by', None)
    query = request.GET.get('q', None)

    if category_slug == 'all':
        goods = Products.objects.all()
    elif query:
        goods = q_search(query)
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    if on_sale:
        goods = goods.filter(discount__gt=0)

    if order_by and order_by != 'default':
        goods = goods.order_by(order_by)

    paginator = Paginator(goods, 3)
    current_page = paginator.page(int(page_number))

    context = {
        "title": "Catalog",
        "goods": current_page,
        "slug_url": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product_obj = Products.objects.get(slug=product_slug)
    context = {
        "product": product_obj,
    }

    return render(request, "goods/product.html", context)

from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404

from goods.models import Products


def catalog(request, category_slug, page_number=1):

    if category_slug == 'all':
        goods = Products.objects.all()
    else:
        goods = get_list_or_404(Products.objects.filter(category__slug=category_slug))

    paginator = Paginator(goods, 3)
    current_page = paginator.page(page_number)

    context = {
        "title": "Catalog",
        "goods": current_page,
        "slug": category_slug,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product_obj = Products.objects.get(slug=product_slug)
    context = {
        "product": product_obj,
    }

    return render(request, "goods/product.html", context)

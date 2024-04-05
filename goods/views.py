from django.shortcuts import render

from goods.models import Products


def catalog(request):
    goods = Products.objects.all()
    context = {
        "title": "Catalog",
        "goods": goods,
    }
    return render(request, "goods/catalog.html", context)


def product(request, product_slug):

    product_obj = Products.objects.get(slug=product_slug)
    context = {
        "product": product_obj,
    }

    return render(request, "goods/product.html", context)

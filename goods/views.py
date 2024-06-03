from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import View
from django.http import JsonResponse

from goods.models import Products, LikedProduct
from goods.utils import q_search


class CatalogView(View):
    template_name = "goods/catalog.html"

    def get(self, request, category_slug=None):
        page_number = request.GET.get('page', 1)
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

        for product in current_page:
            product.likes = product.get_likes()

        context = {
            "title": "Catalog",
            "goods": current_page,
            "slug_url": category_slug,
        }
        return render(request, self.template_name, context)


class ProductView(View):
    template_name = "goods/product.html"

    def get(self, request, product_slug):
        product_obj = get_object_or_404(Products, slug=product_slug)
        product_obj.likes = product_obj.get_likes()
        context = {
            "product": product_obj,
        }
        return render(request, self.template_name, context)


class LikeView(View):

    def post(self, request, product_id):
        product = get_object_or_404(Products, id=product_id)
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'User not authenticated'}, status=403)

        if LikedProduct.objects.filter(user=request.user, product=product).exists():
            product.unlike(request.user)
        else:
            product.like(request.user)

        likes = product.get_likes()
        return JsonResponse({'likes': likes})

from django.core.paginator import Paginator
from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.views import View
from django.http import JsonResponse
from django.views.generic import TemplateView

from goods.models import Products, LikedProduct
from goods.utils import q_search


class CatalogView(TemplateView):
    template_name = "goods/catalog.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        page_number = self.request.GET.get('page', 1)
        on_sale = self.request.GET.get('on_sale', None)
        order_by = self.request.GET.get('order_by', None)
        query = self.request.GET.get('q', None)
        liked_only = self.request.GET.get('liked_only', None)

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

        if liked_only:
            goods = Products.objects.filter(likedproduct__user=self.request.user)

        paginator = Paginator(goods, 3)
        current_page = paginator.page(int(page_number))

        for product in current_page:
            product.likes = product.get_likes()

        context.update({
            "title": "Catalog",
            "goods": current_page,
            "slug_url": category_slug,
        })
        return context


class ProductView(TemplateView):
    template_name = "goods/product.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_slug = self.kwargs.get('product_slug')
        product_obj = get_object_or_404(Products, slug=product_slug)
        product_obj.likes = product_obj.get_likes()
        context.update({
            "product": product_obj,
        })
        return context


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

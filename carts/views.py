from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from carts.models import Cart
from carts.utils import get_user_carts
from goods.models import Products


def cart_add(request):
    product_id = request.GET['product_id']
    product = Products.objects.get(id=product_id)

    if request.user.is_authenticated:
        carts = Cart.objects.filter(user=request.user, product=product)

        if carts.exists():
            cart = carts.first()
            if cart:
                cart.quantity += 1
                cart.save()
        else:
            Cart.objects.create(user=request.user, product=product, quantity=1)

    user_cart = get_user_carts(request.user)

    cart_items_html = render_to_string(
        "carts/includes/included_cart.html", {"cart": user_cart}, request=request
    )

    response = {
        "message": "Carts are added.",
        "cart_items_html": cart_items_html,
    }

    return JsonResponse(response)


def cart_change(request, product_slug):
    ...


def cart_remove(request, cart_id):
    cart = Cart.objects.get(pk=cart_id)
    cart.delete()
    return redirect(request.META['HTTP_REFERER'])

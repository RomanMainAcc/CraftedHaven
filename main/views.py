from django.shortcuts import render

from goods.models import Category


def index(request):
    categories = Category.objects.all()
    context = {
        "title": "CraftedHaven - home page",
        "content": "Furniture store CraftedHaven",
        "categories": categories,
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": "CraftedHaven - about us",
        "content": "About us",
        "text_on_page": "Our furniture is made using the finest materials and meets the highest quality standards."
    }
    return render(request, 'main/about.html', context)

from django.shortcuts import render


def index(request):

    context = {
        "title": "CraftedHaven - home page",
        "content": "Furniture store CraftedHaven",
    }
    return render(request, 'main/index.html', context)


def about(request):
    context = {
        "title": "CraftedHaven - about us",
        "content": "About us",
        "text_on_page": "Our furniture is made using the finest materials and meets the highest quality standards."
    }
    return render(request, 'main/about.html', context)

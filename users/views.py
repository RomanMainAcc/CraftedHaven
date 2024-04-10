from django.shortcuts import render


def login(request):

    context = {
        "title": "CraftedHaven - login",
        "content": "Furniture store CraftedHaven",
    }
    return render(request, 'users/login.html', context)


def registration(request):

    context = {
        "title": "CraftedHaven - login",
        "content": "Furniture store CraftedHaven",
    }
    return render(request, 'users/registration.html', context)


def profile(request):

    context = {
        "title": "CraftedHaven - login",
        "content": "Furniture store CraftedHaven",
    }
    return render(request, 'users/profile.html', context)


def logout(request):

    context = {
        "title": "CraftedHaven - login",
        "content": "Furniture store CraftedHaven",
    }
    return render(request, 'users/login.html', context)

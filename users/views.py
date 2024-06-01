from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Prefetch
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, RedirectView

from orders.models import Order, OrderItem
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm
from carts.models import Cart


class LoginView(View):
    template_name = 'users/login.html'
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class()
        context = {
            "title": "CraftedHaven - login",
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            session_key = request.session.session_key

            if user:
                auth_login(request, user)
                messages.success(request, 'You are now logged in')

                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)

                if 'next' in request.POST:
                    return HttpResponseRedirect(reverse(request.POST['next']))
                return redirect('main:index')

        context = {
            "title": "CraftedHaven - login",
            "form": form,
        }
        return render(request, self.template_name, context)


class RegistrationView(View):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm

    def get(self, request):
        form = self.form_class()
        context = {
            "title": "CraftedHaven - sign in",
            "form": form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth_login(request, user)

            session_key = request.session.session_key
            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, 'You are now registered')
            return HttpResponseRedirect(reverse('main:index'))

        context = {
            "title": "CraftedHaven - sign in",
            "form": form,
        }
        return render(request, self.template_name, context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'users/profile.html'
    form_class = ProfileForm

    def get(self, request):
        form = self.form_class(instance=request.user)
        orders = Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")

        context = {
            'title': 'CraftedHaven - Cabinet',
            'form': form,
            'orders': orders,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(data=request.POST, instance=request.user, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile successfully updated")
            return HttpResponseRedirect(reverse('user:profile'))

        orders = Order.objects.filter(user=request.user).prefetch_related(
            Prefetch(
                "orderitem_set",
                queryset=OrderItem.objects.select_related("product"),
            )
        ).order_by("-id")

        context = {
            'title': 'CraftedHaven - Cabinet',
            'form': form,
            'orders': orders,
        }
        return render(request, self.template_name, context)


class UsersCartView(TemplateView):
    template_name = 'users/users_cart.html'


class LogoutView(LoginRequiredMixin, RedirectView):
    url = reverse_lazy('main:index')

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'You are now logged out')
        return super().get(request, *args, **kwargs)

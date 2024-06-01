from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('users-cart/', UsersCartView.as_view(), name='users_cart'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

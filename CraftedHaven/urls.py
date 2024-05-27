"""
URL configuration for CraftedHaven project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from CraftedHaven import settings
from api.views import CategoryViewSet, ProductsViewSet, UserProfileView

router = DefaultRouter()
router.register(r'category', CategoryViewSet)
router.register(r'products', ProductsViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/profile/', UserProfileView.as_view(), name='user-profile'),
    path('', include("main.urls", namespace="main")),
    path('catalog/', include("goods.urls", namespace="catalog")),
    path('user/', include("users.urls", namespace="user")),
    path('cart/', include("carts.urls", namespace="cart")),
    path('orders/', include("orders.urls", namespace="orders")),

    # path('api/docs/', include_docs_urls(title='Your API Documentation'))


]

if settings.DEBUG:
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from goods.models import Category, Products
from users.models import User


class CategoryViewSetTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        self.client = APIClient()

    def test_anonymous_user_can_list_categories(self):
        response = self.client.get(reverse('category-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_create_category(self):
        response = self.client.post(reverse('category-list'), {'name': 'NewCategory', 'slug': 'new-category'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_category(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('category-list'), {'name': 'NewCategory', 'slug': 'new-category'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_can_update_category(self):
        self.client.login(username='admin', password='password')
        response = self.client.put(reverse('category-detail', args=[self.category.pk]),
                                   {'name': 'UpdatedCategory', 'slug': 'updated-category'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_delete_category(self):
        self.client.login(username='admin', password='password')
        response = self.client.delete(reverse('category-detail', args=[self.category.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ProductsViewSetTests(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_superuser(username='admin', password='password')
        self.regular_user = User.objects.create_user(username='user', password='password')
        self.category = Category.objects.create(name='TestCategory', slug='test-category')
        self.product = Products.objects.create(name='TestProduct', category=self.category, price=100, discount=10)
        self.client = APIClient()

    def test_anonymous_user_can_list_products(self):
        response = self.client.get(reverse('products-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_user_cannot_create_product(self):
        response = self.client.post(reverse('products-list'),
                                    {'name': 'NewProduct', 'category': self.category.id, 'price': 150, 'discount': 15})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_user_can_create_product(self):
        self.client.login(username='admin', password='password')
        response = self.client.post(reverse('products-list'),
                                    {'name': 'NewProduct', 'category': self.category.id, 'price': 150, 'discount': 15})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_admin_user_can_update_product(self):
        self.client.login(username='admin', password='password')
        response = self.client.put(reverse('products-detail', args=[self.product.pk]),
                                   {'name': 'UpdatedProduct', 'category': self.category.id, 'price': 200,
                                    'discount': 20})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_user_can_delete_product(self):
        self.client.login(username='admin', password='password')
        response = self.client.delete(reverse('products-detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class UserProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.client = APIClient()

    def test_authenticated_user_can_retrieve_profile(self):
        self.client.login(username='user', password='password')
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_anonymous_user_cannot_retrieve_profile(self):
        response = self.client.get(reverse('user-profile'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

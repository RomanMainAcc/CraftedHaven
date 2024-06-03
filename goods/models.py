from django.db import models
from CraftedHaven import settings
from users.models import User

redis_instance = settings.redis_instance


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='goods_images/', blank=True, null=True)
    price = models.DecimalField(default=0.0, max_digits=7, decimal_places=2, blank=True, null=True)
    discount = models.DecimalField(default=0.0, max_digits=4, decimal_places=2, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

    def display_id(self):
        return f"{self.id:05}"

    def sell_price(self):
        if self.discount:
            return round(self.price - self.price * self.discount / 100, 2)
        return self.price

    def like(self, user):
        LikedProduct.objects.create(user=user, product=self)
        redis_instance.incr(f"product:{self.id}:likes")

    def unlike(self, user):
        LikedProduct.objects.filter(user=user, product=self).delete()
        redis_instance.decr(f"product:{self.id}:likes")

    def get_likes(self):
        return int(redis_instance.get(f"product:{self.id}:likes") or 0)


class LikedProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user} likes {self.product}"

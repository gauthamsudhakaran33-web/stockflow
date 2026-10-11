from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=150)
    sku = models.CharField(max_length=50, unique=True)
    category = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    reorder_level = models.PositiveIntegerField(default=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

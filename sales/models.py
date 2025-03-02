from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product

User = get_user_model()

class SalesOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('processed', 'Processed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Покупатель
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Продукт
    quantity = models.PositiveIntegerField()  # Количество
    total_price = models.DecimalField(max_digits=10, decimal_places=2)  # Итоговая цена
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')  # Статус заказа
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания
    updated_at = models.DateTimeField(auto_now=True)  # Дата обновления

    def __str__(self):
        return f"Order {self.id} - {self.user.username} - {self.status}"

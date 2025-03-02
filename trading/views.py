from rest_framework import generics, permissions
from .models import Order, Transaction
from .serializers import OrderSerializer, TransactionSerializer

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsTrader
from .models import Order
from .serializers import OrderSerializer

class OrderListCreateView(generics.ListCreateAPIView):
    """
    Размещать ордера могут только трейдеры.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsTrader]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление или удаление конкретного ордера
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class TransactionListView(generics.ListAPIView):
    """
    Получение списка завершённых сделок
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

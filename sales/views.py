from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from trading.serializers import OrderSerializer
from .models import SalesOrder
from .serializers import SalesOrderSerializer

from notifications.utils import send_order_confirmation_email
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from notifications.utils import send_order_confirmation_email

def send_order_notification(order):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "orders",
        {"type": "order_update", "message": f"Новый заказ #{order.id} создан."},
    )

class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save(user=request.user)
            send_order_confirmation_email(request.user.email, order.id)  # Email
            send_order_notification(order)  # WebSocket
            return Response({"message": "Order created successfully."}, status=201)
        return Response(serializer.errors, status=400)

class SalesOrderListCreateView(generics.ListCreateAPIView):
    """
    Получение списка заказов или создание нового заказа
    """
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

class SalesOrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление или удаление конкретного заказа
    """
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer
    permission_classes = [permissions.IsAuthenticated]


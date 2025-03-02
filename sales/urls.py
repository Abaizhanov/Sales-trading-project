from django.urls import path
from .views import SalesOrderListCreateView, SalesOrderDetailView

urlpatterns = [
    path('sales_orders/', SalesOrderListCreateView.as_view(), name='sales-order-list-create'),
    path('sales_orders/<int:pk>/', SalesOrderDetailView.as_view(), name='sales-order-detail'),
]

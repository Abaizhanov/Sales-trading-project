from django.urls import path
from .views import SalesAnalyticsView, SalesPDFReportView
from .views import SalesChartView

urlpatterns = [
    path('sales_report/', SalesAnalyticsView.as_view(), name='sales-report'),
    path('sales_report/pdf/', SalesPDFReportView.as_view(), name='sales-pdf-report'),
    path('sales_chart/', SalesChartView.as_view(), name='sales-chart'),
]
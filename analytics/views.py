import csv
import pandas as pd
from django.http import HttpResponse
from rest_framework import generics, permissions
from sales.models import SalesOrder
from . import models
from .models import AnalyticsReport
from .serializers import AnalyticsReportSerializer
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sales.models import SalesOrder
import matplotlib.pyplot as plt
import io
import base64
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from sales.models import SalesOrder
from django.db.models import Sum


class SalesChartView(APIView):
    """
    Генерация графика продаж
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Используем правильный импорт Sum
        sales = SalesOrder.objects.values('product__name').annotate(total_sales=Sum('quantity'))

        product_names = [sale['product__name'] for sale in sales]
        quantities = [sale['total_sales'] for sale in sales]

        # Создание графика
        plt.figure(figsize=(8, 6))
        plt.bar(product_names, quantities, color='blue')
        plt.xlabel('Продукты')
        plt.ylabel('Количество проданных товаров')
        plt.title('Продажи по продуктам')

        # Сохранение графика в память
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        encoded_image = base64.b64encode(buffer.read()).decode()
        buffer.close()

        return JsonResponse({'chart': encoded_image})

class SalesPDFReportView(APIView):
    """
    Генерация PDF-отчёта по продажам
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        p.setFont("Helvetica", 12)
        p.drawString(100, 750, "Отчёт о продажах")

        y_position = 720  # Начальная позиция текста

        sales = SalesOrder.objects.all()

        for sale in sales:
            text = f"ID: {sale.id}, Пользователь: {sale.user.username}, Товар: {sale.product.name}, Кол-во: {sale.quantity}, Сумма: {sale.total_price}, Статус: {sale.status}"
            p.drawString(100, y_position, text)
            y_position -= 20

            if y_position < 50:  # Переход на новую страницу, если не хватает места
                p.showPage()
                p.setFont("Helvetica", 12)
                y_position = 750

        p.showPage()
        p.save()
        return response


class SalesAnalyticsView(generics.ListAPIView):
    """
    Анализ продаж: общий объём продаж, прибыль и экспорт в CSV
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Загружаем все продажи
        sales_data = SalesOrder.objects.all().values('id', 'user__username', 'product__name', 'quantity', 'total_price', 'status', 'created_at')

        # Конвертируем в DataFrame
        df = pd.DataFrame(sales_data)

        # Генерируем CSV-файл
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'

        df.to_csv(path_or_buf=response, index=False)
        return response

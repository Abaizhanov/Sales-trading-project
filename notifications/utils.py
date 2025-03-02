from django.core.mail import send_mail
from django.conf import settings

def send_order_confirmation_email(user_email, order_id):
    subject = "Подтверждение заказа"
    message = f"Ваш заказ #{order_id} успешно оформлен!"
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user_email],
        fail_silently=False
    )

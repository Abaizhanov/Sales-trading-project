from celery import shared_task

@shared_task
def send_notification_email(email, message):
    print(f"Отправка email на {email}: {message}")
    return f"Email отправлен на {email}"

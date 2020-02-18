from celery import task
from django.core.mail import send_mail
from .models import Order

@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order #{}'.format(order_id)
    message = 'Dear {} {},\n\nYou have successfully placed an order.\nYour order id is {}'.format(order.first_name,
                                                                                                 order.last_name,
                                                                                                 order.id)
    mail_sent = send_mail(subject, message, 'ender3350@gmail.com', [order.email])


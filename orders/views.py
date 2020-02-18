from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderCreateFrom
from . import models
from cart.cart import Cart
from .tasks import order_created
from django.urls import reverse
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(models.Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateFrom(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                models.OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                                                quantity=item['quantity'])
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)

            # set the order in session
            request.session['order_id'] = order.id

            # redirect to payment
            return redirect(reverse('payment:process'))
        else:
            return redirect('orders:order_create')
    else:
        form = OrderCreateFrom()
        return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})



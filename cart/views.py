from django.shortcuts import render, redirect, get_object_or_404
from . import forms
from .cart import Cart
from store import models
from django.views.decorators.http import require_POST
# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Product, id=product_id)
    form = forms.CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product, quantity=cd['quantity'], update_quantity=cd['update'])
        return redirect('cart:cart_detail')
    # else:
    #     return redirect('store:product_details', product_id, product.slug)


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(models.Product, id=product_id)
    cart.remove(product)
    if cart:
        return redirect('cart:cart_detail')
    return redirect('store:products_list')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = forms.CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart, 'len': cart.cart.__len__()})



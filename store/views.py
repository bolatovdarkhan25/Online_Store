from django.shortcuts import render, get_object_or_404, redirect
from . import models
from cart import forms as cart_forms
from cart.cart import Cart
# Create your views here.


def products_list_view(request, category_slug=None):
    category = None
    categories = models.Category.objects.all()
    products = models.Product.objects.filter(available=True)
    cart = Cart(request)
    if category_slug:
        category = get_object_or_404(models.Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product/list.html',
                  {'category': category, 'categories': categories, 'products': products,
                   'cart': cart, 'len': cart.cart.__len__()})


def product_details_view(request, product_id, product_slug):
    product = get_object_or_404(models.Product, id=product_id, slug=product_slug, available=True)
    cart_product_form = cart_forms.CartAddProductForm()
    cart = Cart(request)
    return render(request, 'store/product/details.html', {'product': product, 'cart_product_form': cart_product_form,
                                                          'cart': cart, 'len': cart.cart.__len__()})





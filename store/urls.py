from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.products_list_view, name='products_list'),
    path('category/<slug:category_slug>/', views.products_list_view, name='products_list_by_category'),
    path('product/<int:product_id>/<slug:product_slug>/', views.product_details_view, name='product_details')
]
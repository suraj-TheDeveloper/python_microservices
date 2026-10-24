from django.urls import path
from .views import get_product

urlpatterns = [
    path(
        "products/<int:product_id>/",
        get_product,
        name="get_product"
    ),
]
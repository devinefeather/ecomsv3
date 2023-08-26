from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'app'

urlpatterns = [
    path("", views.index, name="index"),
    path("product/<slug>/", views.product_details, name='product-details'),
    path("add_to_cart", views.add_to_cart, name="add_to_cart"),
    path('view_cart',views.view_cart, name="cart"),
    path('sucess',views.sucess, name="payment_sucess"),
    path('payment-sucess',views.payment_sucess, name="payment-sucess"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

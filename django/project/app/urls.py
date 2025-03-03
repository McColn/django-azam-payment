from django.urls import path
from .views import azampay_payment, payment_success, payment_cancel

urlpatterns = [
    # path("azampay-payment/", azampay_payment, name="azampay_payment"),
    
    path("azampay/", azampay_payment, name="azampay_payment"),
    path("payment-success/", payment_success, name="payment_success"),
    path("payment-cancel/", payment_cancel, name="payment_cancel"),
]

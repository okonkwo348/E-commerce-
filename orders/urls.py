from django.urls import path
from .views import CreatePaymentView, PaymentSuccessView

urlpatterns = [
    path('pay/<int:product_id>/', CreatePaymentView.as_view(), name='create-payment'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment-success'),
]
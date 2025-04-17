from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from .models import Order
from products.models import Product
from .serializers import OrderSerializer
import paypalrestsdk
from django.conf import settings

class CreatePaymentView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
            
            paypalrestsdk.configure({
                "mode": settings.PAYPAL_MODE,
                "client_id": settings.PAYPAL_CLIENT_ID,
                "client_secret": settings.PAYPAL_CLIENT_SECRET
            })
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {"payment_method": "paypal"},
                "redirect_urls": {
                    "return_url": "http://localhost:8000/payment/success/",
                    "cancel_url": "http://localhost:8000/payment/cancel/"
                },
                "transactions": [{
                    "amount": {
                        "total": str(product.price),
                        "currency": "USD"
                    },
                    "description": f"Payment for {product.name}"
                }]
            })

            if payment.create():
                for link in payment.links:
                    if link.rel == "approval_url":
                        approval_url = link.href
                        # Create order
                        order = Order.objects.create(
                            user=request.user,
                            product=product,
                            paypal_payment_id=payment.id
                        )
                        return Response({"payment_url": approval_url, "order_id": order.id})
            else:
                return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

        except Product.DoesNotExist:
            return Response({"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND)

class PaymentSuccessView(views.APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        payment_id = request.GET.get('paymentId')
        payer_id = request.GET.get('PayerID')
        
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            if payment.execute({"payer_id": payer_id}):
                order = Order.objects.get(paypal_payment_id=payment_id)
                order.is_paid = True
                order.save()
                product = order.product
                product.is_paid = True
                product.save()

                return Response({"message": "Payment successful", "order": OrderSerializer(order).data})
            else:
                return Response({"error": payment.error}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
            
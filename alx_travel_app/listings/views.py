import os
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import viewsets
from .models import Booking, Payment
from .serializers import BookingSerializer
from .tasks import send_booking_confirmation_email

# Load Chapa secret key from environment variables
CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")


@api_view(['POST'])
def initiate_payment(request):
    """
    API view to initiate a payment using Chapa payment gateway.
    Creates a Payment object and returns the checkout URL.
    """
    user = request.user
    amount = request.data.get('amount')
    booking_reference = request.data.get('booking_reference')

    # Create a new Payment object with status Pending
    payment = Payment.objects.create(
        user=user,
        amount=amount,
        booking_reference=booking_reference,
        status='Pending'
    )

    # Chapa API endpoint and headers
    chapa_url = "https://api.chapa.co/v1/transaction/initialize"
    headers = {"Authorization": f"Bearer {CHAPA_SECRET_KEY}"}
    data = {
        "amount": str(amount),
        "currency": "ETB",
        "email": user.email,
        "tx_ref": booking_reference,
        "callback_url": "https://yourdomain.com/api/verify-payment/",
        "first_name": user.first_name,
        "last_name": user.last_name,
    }

    # Send request to Chapa API
    response = requests.post(chapa_url, json=data, headers=headers)
    res_data = response.json()

    if response.status_code == 200:
        # Save the transaction ID returned by Chapa
        payment.transaction_id = res_data['data']['id']
        payment.save()
        return JsonResponse({
            "payment_url": res_data['data']['checkout_url'],
            "payment_id": payment.id
        })
    else:
        # Mark payment as failed if API call fails
        payment.status = 'Failed'
        payment.save()
        return JsonResponse(
            {"error": res_data.get('message', 'Payment initiation failed')},
            status=400
        )


class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Booking objects.
    Sends a confirmation email asynchronously using Celery when a booking is created.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def perform_create(self, serializer):
        """
        Called when a new booking is created.
        Saves the booking and triggers the Celery task to send an email.
        """
        booking = serializer.save()

        # Trigger email confirmation asynchronously using Celery
        send_booking_confirmation_email.delay(
            booking.user.email,
            f'Booking ID: {booking.id}, Hotel: {booking.hotel.name}'
        )

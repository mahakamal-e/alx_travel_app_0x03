import os
import requests
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Payment

CHAPA_SECRET_KEY = os.getenv("CHAPA_SECRET_KEY")

@api_view(['POST'])
def initiate_payment(request):
    user = request.user
    amount = request.data.get('amount')
    booking_reference = request.data.get('booking_reference')

    payment = Payment.objects.create(
        user=user,
        amount=amount,
        booking_reference=booking_reference,
        status='Pending'
    )

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

    response = requests.post(chapa_url, json=data, headers=headers)
    res_data = response.json()

    if response.status_code == 200:
        payment.transaction_id = res_data['data']['id']
        payment.save()
        return JsonResponse({
            "payment_url": res_data['data']['checkout_url'],
            "payment_id": payment.id
        })
    else:
        payment.status = 'Failed'
        payment.save()
        return JsonResponse({"error": res_data.get('message', 'Payment initiation failed')}, status=400)

# from django.shortcuts import render
# from django.http import JsonResponse
# import requests
# from .utils import get_azampay_token

# def azampay_payment(request):
#     token = get_azampay_token()
#     if not token:
#         return JsonResponse({"error": "Failed to get access token"}, status=400)

#     url = "https://sandbox.azampay.co.tz/azampay/mno/checkout"
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "accountNumber": "255748121594",  # Replace with actual phone number
#         "additionalProperties": {
#             "property1": None,
#             "property2": None
#         },
#         "amount": "1000",  # Replace with actual amount
#         "currency": "TZS",  # TZS for Tanzanian Shilling
#         "externalId": "123456",  # Unique transaction ID
#         "provider": "Mpesa"
#     }

#     response = requests.post(url, json=payload, headers=headers)

#     if response.status_code == 200:
#         return JsonResponse(response.json())
#     return JsonResponse({"error": "Payment request failed"}, status=400)

# END OF ORIGIN BELOW USE MODEL

from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from .utils import get_azampay_token
from .forms import AzamPayForm
from .models import Payment

def azampay_payment(request):
    if request.method == "POST":
        form = AzamPayForm(request.POST)
        if form.is_valid():
            # Save payment details in database as pending
            payment = form.save(commit=False)
            payment.status = "Pending"
            payment.save()

            token = get_azampay_token()
            if not token:
                payment.status = "Failed"
                payment.save()
                return JsonResponse({"error": "Failed to get access token"}, status=400)

            url = "https://sandbox.azampay.co.tz/azampay/mno/checkout"
            headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            payload = {
                "accountNumber": payment.account_number,
                "additionalProperties": {
                    "property1": None,
                    "property2": None
                },
                "amount": str(payment.amount),
                "currency": payment.currency,
                "externalId": payment.external_id,
                "provider": payment.provider
            }

            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                # Update payment status on success
                response_data = response.json()
                payment.status = "Success"
                payment.transaction_id = response_data.get("transactionId", "")
                payment.save()
                return JsonResponse(response_data)
            else:
                payment.status = "Failed"
                payment.save()
                return JsonResponse({"error": "Payment request failed"}, status=400)
    else:
        form = AzamPayForm()

    return render(request, "app/azampay_payment.html", {"form": form})



def payment_success(request):
    return render(request, "app/payment_success.html")

def payment_cancel(request):
    return render(request, "app/payment_cancel.html")

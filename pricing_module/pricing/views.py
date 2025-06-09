from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
from .models import PricingConfiguration, DistanceBasePrice, DistanceAdditionalPrice, TimeMultiplierFactor, WaitingCharge, Day

@csrf_exempt
def calculate_price(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        distance = float(data.get("distance", 0))
        ride_time = int(data.get("ride_time_minutes", 0))
        waiting_time = int(data.get("waiting_time_minutes", 0))
        date_str = data.get("date")  # Format: YYYY-MM-DD

        ride_date = datetime.strptime(date_str, "%Y-%m-%d")
        weekday = ride_date.strftime('%a')  # Mon, Tue, etc.

        try:
            day_obj = Day.objects.get(code=weekday)
            config = PricingConfiguration.objects.filter(
                is_active=True,
                days_applicable=day_obj,
                valid_from__lte=ride_date,
                valid_to__gte=ride_date
            ).first()

            if not config:
                return JsonResponse({"error": "No active config found for this date"}, status=404)

            # DBP
            dbp = DistanceBasePrice.objects.filter(config=config).order_by('-upto_km').first()
            base_price = float(dbp.price) if distance <= dbp.upto_km else float(dbp.price)

            # DAP
            additional_km = max(0, distance - dbp.upto_km)
            dap = DistanceAdditionalPrice.objects.filter(config=config).order_by('-from_km').first()
            additional_price = additional_km * float(dap.price_per_km)

            # TMF
            tmf = TimeMultiplierFactor.objects.filter(config=config, from_minutes__lte=ride_time, to_minutes__gt=ride_time).first()
            multiplier = float(tmf.multiplier) if tmf else 1.0

            # WC
            wc = WaitingCharge.objects.filter(config=config).first()
            waiting_charge = 0
            if waiting_time > wc.start_after_minutes:
                extra_wait_time = waiting_time - wc.start_after_minutes
                waiting_charge = extra_wait_time * float(wc.rate_per_minute)

            total_price = ((base_price + additional_price) * multiplier) + waiting_charge

            return JsonResponse({
                "base_price": round(base_price, 2),
                "additional_km": round(additional_km, 2),
                "additional_price": round(additional_price, 2),
                "multiplier": multiplier,
                "waiting_charge": round(waiting_charge, 2),
                "total_price": round(total_price, 2)
            })

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return JsonResponse({"error": "Invalid request method"}, status=405)

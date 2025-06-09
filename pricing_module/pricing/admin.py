from django.contrib import admin
from .models import *

admin.site.register(PricingConfiguration)
admin.site.register(Day)
admin.site.register(DistanceBasePrice)
admin.site.register(DistanceAdditionalPrice)
admin.site.register(TimeMultiplierFactor)
admin.site.register(WaitingCharge)
admin.site.register(ConfigChangeLog)

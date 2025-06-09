from django.db import models
from django.contrib.auth.models import User

DAYS_OF_WEEK = [
    ('Mon', 'Monday'),
    ('Tue', 'Tuesday'),
    ('Wed', 'Wednesday'),
    ('Thu', 'Thursday'),
    ('Fri', 'Friday'),
    ('Sat', 'Saturday'),
    ('Sun', 'Sunday'),
]

class PricingConfiguration(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=False)
    valid_from = models.DateField()
    valid_to = models.DateField()
    days_applicable = models.ManyToManyField('Day')

    def __str__(self):
        return self.name

class Day(models.Model):
    code = models.CharField(max_length=3, choices=DAYS_OF_WEEK, unique=True)

    def __str__(self):
        return self.get_code_display()

class DistanceBasePrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name="dbp")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    upto_km = models.FloatField()

class DistanceAdditionalPrice(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name="dap")
    price_per_km = models.DecimalField(max_digits=10, decimal_places=2)
    from_km = models.FloatField()

class TimeMultiplierFactor(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name="tmf")
    from_minutes = models.IntegerField()
    to_minutes = models.IntegerField()
    multiplier = models.FloatField()

class WaitingCharge(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE, related_name="wc")
    start_after_minutes = models.IntegerField()
    rate_per_minute = models.DecimalField(max_digits=10, decimal_places=2)

class ConfigChangeLog(models.Model):
    config = models.ForeignKey(PricingConfiguration, on_delete=models.CASCADE)
    actor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()

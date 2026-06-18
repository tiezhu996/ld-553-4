from django.db import models

from apps.common.constants.enums import PileStatus, PileType


class ChargingPile(models.Model):
    code = models.CharField(max_length=50, unique=True)
    location = models.CharField(max_length=200)
    lat = models.DecimalField(max_digits=10, decimal_places=7)
    lng = models.DecimalField(max_digits=10, decimal_places=7)
    type = models.CharField(max_length=10, choices=PileType.choices)
    power = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=PileStatus.choices, default=PileStatus.IDLE)
    price_per_kwh = models.DecimalField(max_digits=6, decimal_places=2)
    installed_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]


class ChargingRecord(models.Model):
    record_no = models.CharField(max_length=50, unique=True)
    pile = models.ForeignKey(ChargingPile, on_delete=models.CASCADE, related_name="charging_records")
    vehicle = models.ForeignKey("vehicles.Vehicle", on_delete=models.SET_NULL, null=True, blank=True, related_name="charging_records")
    plate_number = models.CharField(max_length=20, blank=True)
    kwh = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField()
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if self.vehicle and not self.plate_number:
            self.plate_number = self.vehicle.plate_number
        super().save(*args, **kwargs)

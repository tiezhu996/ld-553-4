import uuid

from django.db.models import Sum
from django.utils import timezone

from apps.charging.models import ChargingPile, ChargingRecord
from apps.common.constants.enums import PileStatus
from apps.common.exceptions import BusinessException


class ChargingService:
    @staticmethod
    def set_status(pile: ChargingPile, status: str) -> ChargingPile:
        if status == PileStatus.FAULTY and pile.status not in {PileStatus.IDLE, PileStatus.CHARGING}:
            raise BusinessException("只有空闲或充电中的充电桩可以报故障")
        if status == PileStatus.IDLE and pile.status not in {PileStatus.FAULTY, PileStatus.MAINTENANCE}:
            raise BusinessException("只有故障或维护状态可以恢复为空闲")
        pile.status = status
        pile.save(update_fields=["status"])
        return pile

    @staticmethod
    def update_price(pile: ChargingPile, price) -> ChargingPile:
        pile.price_per_kwh = price
        pile.save(update_fields=["price_per_kwh"])
        return pile

    @staticmethod
    def create_record(validated_data: dict) -> ChargingRecord:
        record_no = f"CR{timezone.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:6].upper()}"
        record = ChargingRecord.objects.create(record_no=record_no, **validated_data)
        return record

    @staticmethod
    def today_stats() -> dict:
        today = timezone.now().date()
        records = ChargingRecord.objects.filter(created_at__date=today)
        total_kwh = records.aggregate(total=Sum("kwh"))["total"] or 0
        total_fee = records.aggregate(total=Sum("total_fee"))["total"] or 0
        return {
            "today_charging_kwh": total_kwh,
            "today_charging_revenue": total_fee,
            "today_charging_count": records.count(),
        }

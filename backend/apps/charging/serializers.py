from rest_framework import serializers

from apps.charging.models import ChargingPile, ChargingRecord


class ChargingPileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChargingPile
        fields = "__all__"


class ChargingRecordSerializer(serializers.ModelSerializer):
    pile_detail = ChargingPileSerializer(source="pile", read_only=True)

    class Meta:
        model = ChargingRecord
        fields = "__all__"
        read_only_fields = ["record_no"]

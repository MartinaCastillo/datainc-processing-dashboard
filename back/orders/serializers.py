from rest_framework import serializers

from .models import Order, OrderStatusHistory


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = [
            "status",
            "timestamp",
            "duration_from_previous_seconds",
        ]


class OrderSerializer(serializers.ModelSerializer):
    download_url = serializers.SerializerMethodField()
    processing_duration_seconds = serializers.SerializerMethodField()
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "original_file",
            "processed_file",
            "download_url",
            "status",
            "error_message",
            "records_processed",
            "processing_duration_seconds",
            "status_history",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "processed_file",
            "download_url",
            "status",
            "error_message",
            "records_processed",
            "processing_duration_seconds",
            "status_history",
            "created_at",
            "updated_at",
        ]

    def get_download_url(self, obj):
        request = self.context.get("request")

        if obj.status != Order.Status.DONE or not obj.processed_file:
            return None

        return request.build_absolute_uri(
            f"/api/orders/{obj.id}/download/"
        )

    def get_processing_duration_seconds(self, obj):
        if not obj.started_at or not obj.completed_at:
            return None

        duration = obj.completed_at - obj.started_at

        return round(duration.total_seconds(), 2)
from pathlib import Path

import pandas as pd
from celery import shared_task
from django.utils import timezone

from .models import Order, OrderStatusHistory
from .services.csv_processor import CSVProcessor


def register_status(order, status):
    previous_status = order.status_history.last()

    duration = None

    if previous_status:
        duration = (
            timezone.now() - previous_status.timestamp
        ).total_seconds()

    OrderStatusHistory.objects.create(
        order=order,
        status=status,
        duration_from_previous_seconds=duration,
    )


@shared_task
def process_order(order_id):
    order = Order.objects.get(id=order_id)

    try:
        order.started_at = timezone.now()
        order.status = Order.Status.VERIFYING
        order.error_message = None
        order.save(update_fields=["started_at", "status", "error_message"])

        register_status(order, Order.Status.VERIFYING)

        df = pd.read_csv(order.original_file.path)

        CSVProcessor.validate(df)

        order.status = Order.Status.NORMALIZING
        order.save(update_fields=["status"])

        register_status(order, Order.Status.NORMALIZING)

        df = CSVProcessor.normalize(df)

        processed_dir = Path(order.original_file.path).parent.parent / "processed"
        processed_dir.mkdir(exist_ok=True)

        output_file = processed_dir / f"order_{order.id}.csv"

        df.to_csv(output_file, index=False)

        order.processed_file = f"processed/order_{order.id}.csv"
        order.records_processed = len(df)
        order.completed_at = timezone.now()
        order.status = Order.Status.DONE

        order.save(
            update_fields=[
                "processed_file",
                "records_processed",
                "completed_at",
                "status",
            ]
        )

        register_status(order, Order.Status.DONE)

    except Exception as exc:
        order.status = Order.Status.FAILED
        order.error_message = str(exc)
        order.completed_at = timezone.now()

        order.save(
            update_fields=[
                "status",
                "error_message",
                "completed_at",
            ]
        )

        register_status(order, Order.Status.FAILED)
from django.db import models

class Order(models.Model):
    class Status(models.TextChoices):
        CREATED = "CREATED", "Created"
        VERIFYING = "VERIFYING", "Verifying"
        NORMALIZING = "NORMALIZING", "Normalizing"
        DONE = "DONE", "Done"
        FAILED = "FAILED", "Failed"

    original_file = models.FileField(upload_to="uploads/")
    processed_file = models.FileField(upload_to="processed/", null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CREATED,
    )

    error_message = models.TextField(null=True, blank=True)

    started_at = models.DateTimeField(null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    records_processed = models.IntegerField(
        default=0
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Order #{self.id} - {self.status}"
    
class OrderStatusHistory(models.Model):
    order = models.ForeignKey(
        Order,
        related_name="status_history",
        on_delete=models.CASCADE,
    )

    status = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration_from_previous_seconds = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Order #{self.order_id} - {self.status}"
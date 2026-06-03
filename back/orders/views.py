from django.http import FileResponse
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Order, OrderStatusHistory
from .serializers import OrderSerializer
from .tasks import process_order


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    http_method_names = ["get", "post", "head", "options"]

    def create(self, request, *args, **kwargs):
        uploaded_file = request.FILES.get("original_file")

        if not uploaded_file:
            return Response(
                {"detail": "No file was provided."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not uploaded_file.name.lower().endswith(".csv"):
            return Response(
                {"detail": "Only .csv files are allowed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order = Order.objects.create(
            original_file=uploaded_file,
        )

        OrderStatusHistory.objects.create(
            order=order,
            status=Order.Status.CREATED,
        )

        process_order.delay(order.id)

        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["get"])
    def download(self, request, pk=None):
        order = get_object_or_404(Order, pk=pk)

        if order.status != Order.Status.DONE or not order.processed_file:
            return Response(
                {"detail": "Processed file is not available yet."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return FileResponse(
            order.processed_file.open("rb"),
            as_attachment=True,
            filename=f"order_{order.id}_processed.csv",
        )
from datetime import datetime
from django.utils.timezone import make_aware
from django.db.models import Sum, F
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.pos_systems.models import Order, OrderProduct
from apps.restaurants.models import Restaurant


class DailyReportProductsView(APIView):
    """
    API endpoint to generate daily sales report.
    Filters by date range and restaurant.
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        restaurant_id = request.query_params.get("restaurant")

        # If no date range is provided, default to today
        if not start_date:
            start_date = datetime.today().strftime('%Y-%m-%d')
        if not end_date:
            end_date = start_date

        start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))

        if restaurant_id:
            if not Restaurant.objects.filter(id=restaurant_id,
                                             user=request.user).exists() and not request.user.is_superuser:
                raise PermissionDenied("You do not have access to this restaurant's reports.")
            orders = Order.objects.filter(restaurant_id=restaurant_id, created__date__range=[start_date, end_date])
        else:
            user_restaurants = Restaurant.objects.filter(user=request.user)
            orders = Order.objects.filter(restaurant__in=user_restaurants, created__date__range=[start_date, end_date])

        # Get all order products for the filtered orders
        order_products = OrderProduct.objects.filter(order__in=orders)

        # Group by name and calculate quantity sold and total revenue
        report_data = (
            order_products
            .values(name=F("product__name"))
            .annotate(
                quantity_sold=Sum("quantity"),
                total_revenue=Sum(F("quantity") * F("product__price"))
            )
            .order_by("-quantity_sold")
        )

        return Response({
            "creation_report_date": datetime.today().strftime('%Y-%m-%d'),
            "total_revenue": order_products.aggregate(total_revenue=Sum(F("quantity") * F("product__price")))[
                "total_revenue"],
            "products": list(report_data)
        })

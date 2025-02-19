from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Employee, Restaurant

User = get_user_model()

class VerifyEmployeeEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        restaurant_id = request.data.get('restaurant_id')

        if not email or not restaurant_id:
            return Response(
                {"is_valid": False, "error": "Email and restaurant ID are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Verificar si el usuario es superusuario
        if User.objects.filter(email=email, is_superuser=True).exists():
            return Response({"is_valid": True, "role": "Superuser"}, status=status.HTTP_200_OK)

        # 🔥 Buscar si el restaurante existe
        restaurant = Restaurant.objects.filter(id=restaurant_id).first()
        if not restaurant:
            return Response(
                {"is_valid": False, "error": "Invalid restaurant"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🔥 Buscar si el empleado pertenece al restaurante
        employee = Employee.objects.filter(email=email, restaurant=restaurant).first()

        if employee:
            return Response(
                {
                    "is_valid": True,
                    "restaurant_id": restaurant.id,
                    "restaurant_name": restaurant.name,
                    "role": employee.role
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {"is_valid": False, "error": "Not an employee of this restaurant"},
            status=status.HTTP_403_FORBIDDEN
        )

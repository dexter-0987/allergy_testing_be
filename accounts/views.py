from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from accounts.serializers import CustomTokenObtainPairSerializer
from api.models import Physician


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        username = data.get("username")
        password = data.get("password")
        physician_name = data.get("name")  # Physician full name
        degree = data.get("degree", "MD")  # Default to MD

        if not username or not password:
            return Response(
                {"error": "Username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = User.objects.create(
            username=username,
            email=data.get("email", ""),
            password=make_password(password),
        )

        # Create linked Physician profile
        physician = Physician.objects.create(
            user=user,
            name=physician_name or username,
            degree=degree,
        )

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "physician": {
                        "name": physician.name,
                        "degree": physician.degree,
                    },
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CustomLoginView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_physician(request):
    user = request.user
    physician = getattr(user, "physician_profile", None)
    if not physician:
        return Response({"error": "Physician profile not found"}, status=404)

    return Response(
        {
            "name": physician.name,
            "degree": physician.degree,
        }
    )


class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")

        if not current_password or not new_password:
            return Response({"error": "Both fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(current_password):
            return Response({"error": "Current password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password updated successfully."}, status=status.HTTP_200_OK)

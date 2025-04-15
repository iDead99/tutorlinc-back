from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import UserSerializer
from .models import User
from .utils import send_verification_email, send_password_reset_email

# Optional: for logging
import logging
logger = logging.getLogger(__name__)

class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # ******************* Email verification *******************
    @action(detail=True, methods=["POST", "GET"], permission_classes=[permissions.AllowAny])
    def send_verification(self, request, pk=None):
        user = self.get_object()
        user.generate_verification_token()
        user.save()
        send_verification_email(user)
        logger.info(f"Verification email sent to {user.email}")
        return Response({"message": "Verification email sent!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="verify-email/(?P<token>[^/.]+)", permission_classes=[permissions.AllowAny])
    def verify_email(self, request, token=None):
        try:
            if not token or len(token) < 10:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(verification_token=token)

            if user.is_token_expired():
                return Response({"error": "Token has expired. Please request a new verification email."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.clear_token()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

    # ******************* Password reset *******************
    @action(detail=False, methods=["POST"], url_path="request-password-reset", permission_classes=[permissions.AllowAny])
    def request_password_reset(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.generate_verification_token()
            user.save()
            send_password_reset_email(user)
            logger.info(f"Password reset email sent to {user.email}")
        except User.DoesNotExist:
            pass  # Always respond with success to prevent email discovery

        return Response({"message": "If this email exists, a password reset has been sent."}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["POST"], url_path="confirm-password-reset", permission_classes=[permissions.AllowAny])
    def confirm_password_reset(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response({"error": "Token and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if len(token) < 10:
                return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(verification_token=token)

            if user.is_token_expired():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_password(new_password)
            except ValidationError as e:
                return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.clear_token()
            logger.info(f"Password reset for {user.email}")
            return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

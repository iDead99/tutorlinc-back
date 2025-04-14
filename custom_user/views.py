from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework import viewsets, permissions, status
from .serializers import UserSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import User
from .utils import send_verification_email, send_password_reset_email

class UserViewset(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# *******************Email verification*******************
    @action(detail=True, methods=["POST", "GET"])
    def send_verification(self, request, pk=None):
        user = self.get_object()
        user.generate_verification_token()
        send_verification_email(user)
        return Response({"message": "Verification email sent!"}, status=status.HTTP_200_OK)

    @action(detail=False, methods=["GET"], url_path="verify-email/(?P<token>[^/.]+)")
    def verify_email(self, request, token=None):
        try:
            user = User.objects.get(verification_token=token)
            if user.is_token_expired():
                return Response({"error": "Token has expired. Please request a new verification email."}, status=status.HTTP_400_BAD_REQUEST)

            user.is_active = True
            user.verification_token = None
            user.token_created_at = None
            user.save()
            return Response({"message": "Email verified successfully!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
              return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


# *******************Password reset*******************
    @action(detail=False, methods=["POST"], url_path="request-password-reset")
    def request_password_reset(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(email=email)
            user.generate_verification_token()
            send_password_reset_email(user)
            return Response({"message": "Password reset email sent!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message": "If this email exists, a password reset has been sent."}, status=200)

    @action(detail=False, methods=["POST"], url_path="confirm-password-reset")
    def confirm_password_reset(self, request):
        token = request.data.get("token")
        new_password = request.data.get("new_password")

        if not token or not new_password:
            return Response({"error": "Token and new password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Find the user associated with the token
            user = User.objects.get(verification_token=token)

            if user.is_token_expired():
                return Response({"error": "Token has expired."}, status=status.HTTP_400_BAD_REQUEST)

            # Validate the new password
            try:
                validate_password(new_password)  # This validates the password based on Django's rules
            except ValidationError as e:
                return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

            # Reset password
            user.set_password(new_password)
            user.verification_token = None
            user.token_created_at = None
            user.save()

            return Response({"message": "Password reset successful!"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)

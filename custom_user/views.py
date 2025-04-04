from datetime import timedelta
from django.utils.timezone import now
import random
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets, permissions, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .models import User
from .serializers import UserSerializer
from .utils import send_verification_email  # Import email function

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['GET', 'PUT', 'PATCH'])
    def send_verification_code(self, request, pk=None):
        print(f"📌 View accessed: send_verification_code for user ID {pk}")  # Debug print

        try:
            user = self.get_object()
            print(f"✅ User found: {user.email}")  # Debug print
        except User.DoesNotExist:
            print("❌ User not found!")  # Debug print
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        if request.method == 'GET':
            print("📩 GET request received")  # Debug print

            # **Check if the verification code is expired**
            if not user.is_verification_code_valid():
                return Response(
                    {'error': 'Verification code expired. Please request a new one.', 'expired': True},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = UserSerializer(user)
            return Response(serializer.data)

        elif request.method in ['PUT', 'PATCH']:
            print("📩 PUT/PATCH request received")  # Debug print
            
            # Generate a new verification code and expiry time
            user.generate_verification_code()
            user.save()

            print("📤 Sending email...")  # Debug print
            email_sent = send_verification_email(user)  # Check if email was sent

            if not email_sent:
                return Response(
                    {'error': 'Failed to send verification email. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response({
                'message': 'Verification code sent. This code expires in 5 minutes.',
                'user': serializer.data
            }, status=status.HTTP_200_OK)

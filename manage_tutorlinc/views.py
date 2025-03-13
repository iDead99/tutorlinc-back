from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Teacher, Subject, Address, Verification, Inquiry, Comment
from .serializers import (
    TeacherSerializer,
    SubjectSerializer,
    AddressSerializer,
    VerificationSerializer,
    InquirySerializer,
    CommentSerializer,
)

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.select_related('user').prefetch_related('subject_set').all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['user__id']
    search_fields = ['user__first_name', 'user__last_name', 'phone']

    @action(detail=False, methods=['GET', 'PUT', 'PATCH'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        teacher = Teacher.objects.get(user_id=request.user.id)
        
        if request.method == 'GET':
            serializer = TeacherSerializer(teacher)
            return Response(serializer.data)
        elif request.method in ['PUT', 'PATCH']:
            serializer = TeacherSerializer(
                teacher, data=request.data, partial=(request.method == 'PATCH')
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.select_related('teacher').all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['teacher__id']
    search_fields = ['name']

class AddressViewSet(viewsets.ModelViewSet):
    queryset = Address.objects.select_related('teacher').all()
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['teacher__id']
    search_fields = ['region', 'town', 'street']

class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.select_related('teacher').all()
    serializer_class = VerificationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.select_related('teacher').all().order_by('-id')
    serializer_class = InquirySerializer
    permission_classes = [permissions.AllowAny]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['teacher__id']

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentSerializer

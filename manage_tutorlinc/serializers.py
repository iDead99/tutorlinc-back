from rest_framework import serializers
from .models import Teacher, Subject, Address, Verification, Inquiry, Comment
from custom_user.serializers import UserSerializer

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'user', 'phone', 'gender', 'bio', 'highest_qualification', 'availability_status', 'profile_picture']

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'price', 'day_to_teach', 'start_time', 'end_time', 'teacher']
        read_only_fields = ['teacher']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        validated_data['teacher'] = Teacher.objects.get(user=user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.teacher.user != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to modify this data.")
        return super().update(instance, validated_data)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['region', 'town', 'street', 'teacher']
        read_only_fields = ['teacher']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        validated_data['teacher'] = Teacher.objects.get(user=user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.teacher.user != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to modify this data.")
        return super().update(instance, validated_data)

class VerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Verification
        fields = ['id_card', 'id_verification', 'certificate', 'teacher']
        read_only_fields = ['teacher']

    def create(self, validated_data):
        user = self.context['request'].user
        if not user.is_authenticated:
            raise serializers.ValidationError("Authentication required.")
        validated_data['teacher'] = Teacher.objects.get(user=user)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if instance.teacher.user != self.context['request'].user:
            raise serializers.ValidationError("You do not have permission to modify this data.")
        return super().update(instance, validated_data)

class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'student_name', 'email', 'phone', 'message', 'teacher']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'comment', 'commenter', 'rate']

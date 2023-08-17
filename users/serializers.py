from rest_framework import serializers
from users.models import User
from reports.models import Report
from django.core.validators import RegexValidator


class UserSerializer(serializers.ModelSerializer):
    reports = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Report.objects.all(), required=False
    )
    email = serializers.EmailField(required=False)
    full_name = serializers.CharField(required=False)
    contact_number = serializers.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r"^(\d{2,3}-)?\d{3,4}-\d{4}$",
                message="유효한 전화번호 형식이 아닙니다.",
            )
        ],
    )
    isAgree = serializers.BooleanField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "email",
            "full_name",
            "contact_number",
            "isAgree",
            "reports",
        ]

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        if password:
            instance.set_password(password)
        return super().update(instance, validated_data)

    def to_representation(self, instance):  # 마이페이지 데이터 전달
        return {
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "full_name": instance.full_name,
            "contact_number": instance.contact_number,
            "isAgree": instance.isAgree,
            "reports": [
                {"id": report.id, "report_title": report.report_title}
                for report in instance.reports.filter(is_deleted=False)
            ],
        }

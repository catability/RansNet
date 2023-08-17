from rest_framework import serializers
from reports.models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = [
            "id",
            "report_account",
            "report_title",
            "reporter_name",
            "reporter_contact",
            "reporter_email",
            "accident_time",
            "cognition_time",
            "total_pc",
            "total_server",
            "damaged_pc",
            "damaged_server",
            "accident_details",
            "action_details",
            "encrypted_file_ext",
            "current_status",
            "backup_status",
            "ransom_status",
            "report_status",
        ]

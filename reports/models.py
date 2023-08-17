from django.db import models
from django.core.validators import EmailValidator, MinValueValidator, RegexValidator


phone_number_validator = RegexValidator(
    regex=r"^(\d{2,3}-)?\d{3,4}-\d{4}$", message="유효한 전화번호 형식이 아닙니다."
)
email_validator = EmailValidator(
    message="유효한 이메일 주소 형식이 아닙니다."
    # 기본 검증은 @와 .의 유무
    # allowlist=['example.com','예시.도메인','등등']
)
number_validator = MinValueValidator(0, message="양수만 입력 가능합니다.")


class Report(models.Model):
    report_account = models.ForeignKey(
        verbose_name="신고 계정",
        to="users.User",
        related_name="reports",
        null=True,
        on_delete=models.SET_NULL,
    )
    report_title = models.CharField(verbose_name="신고 제목", max_length=128, null=False)

    reporter_name = models.CharField(verbose_name="신고자 이름", max_length=8, null=False)
    reporter_contact = models.CharField(
        verbose_name="신고자 연락처",
        max_length=16,
        null=False,
        validators=[phone_number_validator],
    )
    reporter_email = models.EmailField(
        verbose_name="신고자 메일", null=False, validators=[email_validator]
    )

    # 날짜 형식 해결 필요
    created_time = models.DateTimeField(verbose_name="신고접수시간", auto_now_add=True)
    updated_time = models.DateTimeField(verbose_name="신고수정시간", auto_now=True)
    accident_time = models.DateTimeField(verbose_name="사고발생시간", null=True)
    cognition_time = models.DateTimeField(verbose_name="사고인지시점", null=True)

    total_pc = models.IntegerField(
        verbose_name="전체pc대수", null=False, validators=[number_validator]
    )
    total_server = models.IntegerField(
        verbose_name="전체서버대수", null=False, validators=[number_validator]
    )
    damaged_pc = models.IntegerField(
        verbose_name="피해pc대수", null=False, validators=[number_validator]
    )
    damaged_server = models.IntegerField(
        verbose_name="피해서버대수", null=False, validators=[number_validator]
    )

    accident_details = models.TextField(verbose_name="사고내용", blank=True, null=False)
    action_details = models.TextField(verbose_name="조치사항", blank=True, null=False)
    encrypted_file_ext = models.CharField(
        verbose_name="암호화파일 확장자명", max_length=8, null=False
    )

    # 기타 선택 시 입력데이터 저장 해결 필요
    CURRENT_STATUS = [
        ("단순업무장애", "단순업무장애"),
        ("주요서비스장애", "주요서비스장애"),
        ("개인정보유출", "개인정보유출"),
        ("기타", "기타"),
    ]
    current_status = models.CharField(
        verbose_name="피해현황", max_length=16, choices=CURRENT_STATUS, null=False
    )

    BACKUP_STATUS = [
        ("전체백업", "전체백업"),
        ("일부백업", "일부백업"),
        ("백업이 있으나 감염", "백업이 있으나 감염"),
        ("없음", "없음"),
        ("기타", "기타"),
    ]
    backup_status = models.CharField(
        verbose_name="백업유무", max_length=16, choices=BACKUP_STATUS, null=False
    )

    ransom_status = models.BooleanField(verbose_name="협박유무", null=False)
    report_status = models.BooleanField(verbose_name="경찰신고 유무", null=False)

    is_deleted = models.BooleanField(verbose_name="신고삭제 유무", default=False)

    def __str__(self):
        return self.report_title

    class Meta:
        db_table = "report"

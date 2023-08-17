from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

phone_number_validator = RegexValidator(
    regex=r"^(\d{2,3}-)?\d{3,4}-\d{4}$", message="유효한 전화번호 형식이 아닙니다."
)


class User(AbstractUser):
    # username
    # password
    # email
    full_name = models.CharField(verbose_name="이름", max_length=8, blank=True)
    contact_number = models.CharField(
        verbose_name="연락처",
        max_length=16,
        blank=True,
        validators=[phone_number_validator],
    )
    isAgree = models.BooleanField(verbose_name="동의여부", default=False)

    class Meta:
        db_table = "user"

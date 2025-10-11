import uuid
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    """Customized user manager"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    """Customized User model"""

    username = None
    email = models.EmailField(
        "email address",
        unique=True,
        error_messages={"unique": "A user with that email already exists."},
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


class RepairRecord(models.Model):
    CONDITION_CHOICES = [
        ("satisfactory", "Satisfactory"),
        ("unsatisfactory", "Unsatisfactory"),
    ]

    department_name = models.CharField(max_length=255)
    user_name = models.CharField(
        max_length=255, help_text="Person who brought the device"
    )
    hardware_type = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    nature_of_complaint = models.TextField()
    ict_personnel = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repair_records",
        help_text="Logged-in ICT staff handling this repair",
    )
    maintenance_action_taken = models.TextField(blank=True, null=True)
    department_email = models.EmailField()
    confirmation_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True
    )
    condition_after_repair = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text="To be filled by department after repair",
    )
    signature = models.CharField(
        max_length=255, blank=True, null=True, help_text="Filled by department"
    )
    is_confirmed = models.BooleanField(default=False)
    slug = models.SlugField(unique=True, blank=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Repair Record"
        verbose_name_plural = "Repair Records"

    def __str__(self):
        return f"{self.department_name} - {self.hardware_type} ({self.user_name})"

    def mark_confirmed(self):
        """Mark the record as confirmed."""
        self.is_confirmed = True
        self.save()

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.department_name}-{self.hardware_type}")
            slug = base_slug
            counter = 1
            while RepairRecord.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

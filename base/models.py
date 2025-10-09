import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class RepairRecord(models.Model):
    CONDITION_CHOICES = [
        ('satisfactory', 'Satisfactory'),
        ('unsatisfactory', 'Unsatisfactory'),
    ]

    department_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255, help_text="Person who brought the device")
    hardware_type = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    nature_of_complaint = models.TextField()
    ict_personnel = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="repair_records",
        help_text="Logged-in ICT staff handling this repair"
    )
    maintenance_action_taken = models.TextField(blank=True, null=True)
    department_email = models.EmailField()
    confirmation_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    condition_after_repair = models.CharField(
        max_length=20,
        choices=CONDITION_CHOICES,
        blank=True,
        null=True,
        help_text="To be filled by department after repair"
    )
    signature = models.CharField(max_length=255, blank=True, null=True, help_text="Filled by department")
    is_confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Repair Record"
        verbose_name_plural = "Repair Records"

    def __str__(self):
        return f"{self.department_name} - {self.hardware_type} ({self.user_name})"

    def mark_confirmed(self):
        """Mark the record as confirmed."""
        self.is_confirmed = True
        self.save()

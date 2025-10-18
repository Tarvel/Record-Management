import csv
import io

from django.contrib import admin, messages
from django.shortcuts import render, redirect
from django.urls import path

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .forms import CustomUserCreationForm, CustomUserChangeForm, CsvUploadForm
from .models import CustomUser, RepairRecord


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ["email", "first_name", "last_name", "is_staff"]

    search_fields = ("email", "first_name", "last_name")

    ordering = ("email",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "first_name",
                    "last_name",
                    "email",
                    "password1",
                    "password2",
                ),
            },
        ),
    )

    def get_urls(self):
        """Adds the custom URL for our upload page."""
        urls = super().get_urls()
        custom_urls = [
            path(
                "upload-csv/",
                self.admin_site.admin_view(self.upload_csv_view),
                name="upload_csv",
            ),
        ]
        return custom_urls + urls

    def upload_csv_view(self, request):
        """This view handles the CSV upload page and logic."""
        if request.method == "POST":
            form = CsvUploadForm(request.POST, request.FILES)
            if form.is_valid():

                csv_file = request.FILES["csv_file"]
                decoded_file = csv_file.read().decode("utf-8")
                io_string = io.StringIO(decoded_file)

                reader = csv.DictReader(io_string)
                users_created = 0
                users_skipped = 0

                for row in reader:
                    email = row.get("email")
                    first_name = row.get("first_name")
                    last_name = row.get("last_name")

                    if not email or not last_name:
                        messages.error(
                            request,
                            f"Skipping row cos of missing email or last name: {row}",
                        )
                        continue

                    if CustomUser.objects.filter(email=email).exists():
                        users_skipped += 1
                        continue

                    try:
                        CustomUser.objects.create_user(
                            email=email,
                            first_name=first_name,
                            last_name=last_name,
                            password=f"UITH-STAFF-{last_name.upper()}",
                        )
                        users_created += 1
                    except Exception as e:
                        messages.error(request, f"Error creating user {email}: {e}")

                self.message_user(
                    request, f"Successfully created {users_created} new users."
                )
                if users_skipped > 0:
                    self.message_user(
                        request,
                        f"Skipped {users_skipped} users bcause they already exist.",
                        level=messages.WARNING,
                    )

                return redirect("..")

        form = CsvUploadForm()
        context = {"form": form}
        return render(request, "admin/csv_upload.html", context)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(RepairRecord)

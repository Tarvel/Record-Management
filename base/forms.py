from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from django import forms
from django.core.validators import FileExtensionValidator


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = (
            "first_name",
            "last_name",
            "email",
        )


class CsvUploadForm(forms.Form):
    csv_file = forms.FileField(
        label="Upload CSV File",
        validators=[FileExtensionValidator(allowed_extensions=["csv"])],
    )


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=150)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())


from django import forms
from django.contrib.auth.forms import PasswordChangeForm


class TailwindPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs.update(
                {
                    "class": (
                        "w-full px-4 py-2 bg-white "
                        "border border-slate-300 "
                        "rounded-lg focus:outline-none focus:ring-2 "
                        "focus:ring-green-500 transition-colors"
                    ),
                    "placeholder": field.label,
                }
            )

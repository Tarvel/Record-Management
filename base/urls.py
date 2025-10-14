from django.contrib.auth import views as auth_views
from .forms import TailwindPasswordChangeForm
from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboardPage, name="dashboard"),
    path("record/<str:slug>", views.recordDetail, name="record_detail"),
    path("record/create/", views.createRecord, name="create_record"),
    path(
        "confirmation/<str:confirmation_token>",
        views.confirmationPage,
        name="confirmation_page",
    ),
    path(
        "password/change/",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html",
        ),
        name="password_change",
    ),
    path("password/change/done", views.password_change_done, name="password_change_done"),
    path("confirmation/success/", views.sucessPage, name="success"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
]
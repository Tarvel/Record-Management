from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboardPage, name="dashboard"),
    path("record/", views.recordDetail, name="record_detail"),
    path("record/create/", views.createRecord, name="create_record"),
    path("confirmation/", views.confirmationPage, name="confirmation_page"),
    path("invalid-token/", views.invalidTokenPage, name="invalid_token"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout")
]

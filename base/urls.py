from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboardPage, name="dashboard"),
    path("record/<str:slug>", views.recordDetail, name="record_detail"),
    path("record/create/", views.createRecord, name="create_record"),
    path("confirmation/<str:confirmation_token>", views.confirmationPage, name="confirmation_page"),
    path("confirmation/success/", views.sucessPage, name="success"),
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutPage, name="logout"),
]

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# @login_required
def dashboardPage(request):
    return render(request, "base/dashboard.html")


# @login_required
def recordDetail(request):
    return render(request, "base/detail_view.html")


# @login_required
def createRecord(request):
    page = "create"

    context = {
        "page": page,
    }
    return render(request, "base/create_record.html", context)


def confirmationPage(request):
    return render(request, "base/confirmation_page.html")


def invalidTokenPage(request):
    return render(request, "base/invalid_token.html")


def loginPage(request):
    return render(request, "base/login.html")

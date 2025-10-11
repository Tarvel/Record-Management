from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm


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
    form = LoginForm()
    method = request.method
    if method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now signed in as {email}")
                next_url = request.POST.get("next") or "dashboard"
                return redirect(next_url)
            else:
                messages.error(request, "ERROR, invalid credentials")
                return redirect("login")

        else:
            form = LoginForm()

    context = {
        "form": form,
        "next": request.GET.get("next", ""),
    }
    return render(request, "base/login.html", context)

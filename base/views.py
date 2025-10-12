from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import LoginForm
from .models import RepairRecord


@login_required(login_url="login")
def dashboardPage(request):
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    date = request.GET.get("date", "")

    records = RepairRecord.objects.all()

    if search:
        records = (
            records.filter(department__icontains=search)
            | records.filter(user_name__icontains=search)
            | records.filter(ict_personnel__icontains=search)
        )
    if status and status != "All":
        records = records.filter(status=status)
    if date:
        records = records.filter(date=date)

    paginator = Paginator(records, 5)
    page = request.GET.get("page", 1)
    record_obj = paginator.get_page(page)

    context = {
        "records": record_obj,
    }

    if request.htmx:
        return render(request, "base.partials/dashboard_htmx.html", context)

    return render(request, "base/dashboard.html", context)


@login_required(login_url="login")
def recordDetail(request):
    return render(request, "base/detail_view.html")


@login_required(login_url="login")
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


@login_required(login_url="login")
def logoutPage(request):
    logout(request)
    return redirect("home")

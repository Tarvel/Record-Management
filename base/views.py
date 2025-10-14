from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import LoginForm, RepairRecordForm
from .models import RepairRecord
from django.urls import reverse
from .utils.emails import (
    send_create_confirmation_email_async,
    send_return_confirmation_email_async,
)


@login_required(login_url="login")
def dashboardPage(request):
    page = "dashboard"
    search = request.GET.get("search", "")
    status = request.GET.get("status", "")
    date = request.GET.get("date", "")

    records = RepairRecord.objects.all()

    if search:
        records = (
            records.filter(department_name__icontains=search)
            | records.filter(user_name__icontains=search)
            | records.filter(ict_personnel__first_name__icontains=search)
            | records.filter(ict_personnel__last_name__icontains=search)
            | records.filter(hardware_type__icontains=search)
        )
    if status and status != "All":
        if status == "Pending Confirmation":
            records = records.filter(is_confirmed=False)
        elif status == "Confirmed":
            records = records.filter(is_confirmed=True)
        else:
            records = (
                records.filter(department_name__icontains=search)
                | records.filter(user_name__icontains=search)
                | records.filter(ict_personnel__first_name__icontains=search)
                | records.filter(ict_personnel__last_name__icontains=search)
            )
    if date:
        print(date)
        records = records.filter(updated_at__date=date)

    paginator = Paginator(records, 6)
    pages = request.GET.get("page", 1)
    record_obj = paginator.get_page(pages)

    context = {
        "page": page,
        "search": search,
        "status": status,
        "date": date,
        "records": record_obj,
    }

    if request.htmx:
        return render(request, "base/partials/dashboard_htmx.html", context)

    return render(request, "base/dashboard.html", context)


@login_required(login_url="login")
def recordDetail(request, slug):
    record = RepairRecord.objects.get(slug=slug)

    context = {"record": record}
    return render(request, "base/detail_view.html", context)


@login_required(login_url="login")
def createRecord(request):
    page = "create"
    form = RepairRecordForm()
    if request.method == "POST":
        form = RepairRecordForm(request.POST)
        if form.is_valid():
            print(request.POST)
            record = form.save(commit=False)
            record.ict_personnel = request.user
            record.save()

            confirmation_path = reverse(
                "confirmation_page",
                kwargs={"confirmation_token": record.confirmation_token},
            )
            confirmation_link = request.build_absolute_uri(confirmation_path)

            send_create_confirmation_email_async(
                to_email=record.department_email,
                confirmation_link=confirmation_link,
                hardware_type=record.hardware_type,
            )
            messages.success(
                request,
                f"An email has been sent to {record.department_email} for confirmation",
            )
            return redirect("dashboard")
    else:
        form = RepairRecordForm()

    context = {
        "page": page,
        "form": form,
    }
    return render(request, "base/create_record.html", context)


def confirmationPage(request, confirmation_token):
    record = RepairRecord.objects.get(confirmation_token=confirmation_token)
    if record.is_confirmed:
        return render(request, "base/invalid_token.html")
    if request.method == "POST":
        condition = request.POST.get("condition")
        signature = request.POST.get("signature")

        record.signature = signature
        record.is_confirmed = True
        record.condition_after_repair = condition
        record.save()

        record_url_path = reverse(
            "record_detail",
            kwargs={"slug": record.slug},
        )
        record_url = request.build_absolute_uri(record_url_path)
        print(record.ict_personnel.email, record_url)
        send_return_confirmation_email_async(
            to_email=record.ict_personnel.email,
            record_url=record_url,
            record=record,
        )

        return redirect("success")

    return render(request, "base/confirmation_page.html", {"record": record})


def sucessPage(request):
    return render(request, "base/success.html")


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
                messages.error(request, "ERROR, Invalid Credentials")
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
    return redirect("login")


def password_change_done(request):
    messages.success(request, "Password change successfully!")
    return redirect("dashboard")

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
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

    records = RepairRecord.objects.select_related("ict_personnel").filter(
        is_published=True
    )

    if search:
        records = records.filter(
            Q(department_name__icontains=search)
            | Q(user_name__icontains=search)
            | Q(ict_personnel__first_name__icontains=search)
            | Q(ict_personnel__last_name__icontains=search)
            | Q(hardware_type__icontains=search)
        )

    if status and status != "All":
        if status == "Pending Confirmation":
            records = records.filter(is_confirmed=False)
        elif status == "Confirmed":
            records = records.filter(is_confirmed=True)

    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            records = records.filter(updated_at__date=parsed_date)
        except ValueError:
            pass

    paginator = Paginator(records, 6)
    page_number = request.GET.get("page", 1)
    record_obj = paginator.get_page(page_number)

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
def draftPage(request):
    page = "drafts"
    search = request.GET.get("search", "")
    date = request.GET.get("date", "")

    records = RepairRecord.objects.select_related("ict_personnel").filter(
        is_published=False  # , ict_personnel=request.user
    )

    if search:
        records = records.filter(
            Q(department_name__icontains=search)
            | Q(user_name__icontains=search)
            | Q(ict_personnel__first_name__icontains=search)
            | Q(ict_personnel__last_name__icontains=search)
            | Q(hardware_type__icontains=search)
        )

    if date:
        try:
            parsed_date = datetime.strptime(date, "%Y-%m-%d").date()
            records = records.filter(updated_at__date=parsed_date)
        except ValueError:
            pass

    paginator = Paginator(records, 6)
    page_number = request.GET.get("page", 1)
    record_obj = paginator.get_page(page_number)

    context = {
        "page": page,
        "search": search,
        "date": date,
        "records": record_obj,
    }

    if request.htmx:
        return render(request, "base/partials/dashboard_htmx.html", context)
    return render(request, "base/dashboard.html", context)


def draftDetail(request, slug):
    record = RepairRecord.objects.get(slug=slug)

    context = {"record": record}
    return render(request, "base/draft_detail.html", context)


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
            action = request.POST.get("action")

            if action == "save_draft":
                record.is_published = False
                record.save()
                messages.success(
                    request,
                    "Record added to drafts!",
                )
                return redirect("dashboard")

            elif action == "publish":
                print("Publish button was clicked!")
                record.is_published = True
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


@login_required(login_url="login")
def editDraft(request, slug):
    page = "edit"
    repair_record_obj = get_object_or_404(RepairRecord, slug=slug, is_published=False)
    form = RepairRecordForm(instance=repair_record_obj)
    if request.method == "POST":
        form = RepairRecordForm(request.POST)
        if form.is_valid():
            print(request.POST)
            record = form.save(commit=False)
            record.ict_personnel = request.user
            record.is_published = True
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
        form = RepairRecordForm(instance=repair_record_obj)

    context = {
        "record": repair_record_obj,
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
        import logging

        logger = logging.getLogger(__name__)
        print("RENDER LOG TEST: View was hit!")
        logger.warning("RENDER LOGGER TEST: View was definitely hit!")
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


@login_required(login_url="login")
def password_change_done(request):
    messages.success(request, "Password change successfully!")
    return redirect("dashboard")


@login_required(login_url="login")
def deleteDraft(request, slug):
    repair_record_obj = get_object_or_404(
        RepairRecord, slug=slug, is_published=False, ict_personnel=request.user
    )
    messages.success(
        request,
        f"Draft for {repair_record_obj.hardware_type} from {repair_record_obj.department_name} has been deleted",
    )
    repair_record_obj.delete()
    return redirect("dashboard")

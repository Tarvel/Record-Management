from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import strip_tags
import logging
import threading

logger = logging.getLogger(__name__)


def _send_email(subject: str, to_email: str, html_template: str, context: dict) -> bool:
    """Handles rendering and sending HTML + text email."""
    try:
        html_content = render_to_string(html_template, context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject.title(),
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)  # False for debugging/testing

        logger.info("Email '%s' sent to %s", subject, to_email)
        return True
    except Exception as exc:
        logger.exception("Failed to send email '%s' to %s: %s", subject, to_email, exc)
        return False


def send_create_confirmation_email(to_email: str, confirmation_link: str, hardware_type: str) -> bool:
    context = {
        "current_date": timezone.now(),
        "confirmation_link": confirmation_link,
        "hardware_type": hardware_type,
    }
    return _send_email("Please confirm your repair", to_email, "emails/email_confirmation.html", context)


def send_return_confirmation_email(to_email: str, record_url: str, record: str) -> bool:
    context = {
        "current_date": timezone.now(),
        "record_url": record_url,
        "record": record,
    }
    return _send_email("Repair Confirmation Received", to_email, "emails/email_return.html", context)


def send_create_confirmation_email_async(to_email, confirmation_link, hardware_type):
    threading.Thread(
        target=send_create_confirmation_email,
        args=(to_email, confirmation_link, hardware_type),
        daemon=True,
    ).start()


def send_return_confirmation_email_async(to_email, record_url, record):
    threading.Thread(
        target=send_return_confirmation_email,
        args=(to_email, record_url, record),
        daemon=True,
    ).start()

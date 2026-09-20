import smtplib
from email.message import EmailMessage

from app.core.config import settings


def send_critical_alert_email(
    recipient_email: str,
    storage_unit_id: int,
    temperature: float,
    message: str
):
    print(">>> COLDGUARD EMAIL FUNCTION CALLED")
    print(f">>> Recipient: {recipient_email}")
    print(f">>> Storage Unit: {storage_unit_id}")
    print(f">>> Temperature: {temperature}°C")

    email = EmailMessage()

    email["Subject"] = (
        f"ColdGuard Critical Temperature Alert - Unit {storage_unit_id}"
    )

    email["From"] = settings.SMTP_EMAIL
    email["To"] = recipient_email

    email.set_content(
        f"""ColdGuard Critical Temperature Alert

Storage Unit: {storage_unit_id}
Temperature: {temperature}°C

Alert:
{message}

Please check the storage unit immediately.
"""
    )

    print(">>> Connecting to SMTP server...")

    with smtplib.SMTP(
        settings.SMTP_HOST,
        settings.SMTP_PORT
    ) as server:

        print(">>> Starting TLS...")
        server.starttls()

        print(">>> Logging into SMTP...")
        server.login(
            settings.SMTP_EMAIL,
            settings.SMTP_PASSWORD
        )

        print(">>> Sending email...")
        server.send_message(email)

    print(">>> COLDGUARD EMAIL SENT SUCCESSFULLY")
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)


def send_order_confirmation_email(
    email: str,
    order_id: int,
    total_amount: float,
    customer_name: str
) -> bool:
    """
    Send order confirmation email to customer.

    In development, this will just log the email content.
    In production, configure SMTP settings via environment variables.
    """
    subject = f"Order Confirmation - Order #{order_id}"

    # Create HTML email body
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #2c1810;
                color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .order-details {{
                background-color: white;
                padding: 15px;
                margin: 20px 0;
                border-radius: 5px;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 12px;
                color: #666;
            }}
            .total {{
                font-size: 24px;
                font-weight: bold;
                color: #d4a574;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Leather Accessories Store</h1>
            </div>
            <div class="content">
                <h2>Thank you for your order!</h2>
                <p>Dear {customer_name},</p>
                <p>We're pleased to confirm that we've received your order.</p>

                <div class="order-details">
                    <h3>Order Details</h3>
                    <p><strong>Order Number:</strong> #{order_id}</p>
                    <p><strong>Total Amount:</strong> <span class="total">${total_amount:.2f}</span></p>
                </div>

                <p>We'll send you another email when your order ships.</p>
                <p>If you have any questions, please don't hesitate to contact us.</p>

                <p>Thank you for shopping with us!</p>
                <p>Best regards,<br>The Leather Accessories Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 Leather Accessories Store. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    # In development, just log the email
    if not settings.SMTP_PASSWORD:
        logger.info(f"[DEV] Order confirmation email for {email}:")
        logger.info(f"Subject: {subject}")
        logger.info(f"Order ID: {order_id}, Total: ${total_amount:.2f}")
        print(f"\n{'='*60}")
        print(f"📧 ORDER CONFIRMATION EMAIL")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Subject: {subject}")
        print(f"Order #: {order_id}")
        print(f"Total: ${total_amount:.2f}")
        print(f"Customer: {customer_name}")
        print(f"{'='*60}\n")
        return True

    # In production, send actual email
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Leather Accessories Store <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = email

        # Attach HTML body
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        logger.info(f"Attempting to send order confirmation email to {email} via {settings.SMTP_HOST}:{settings.SMTP_PORT}")

        # Send email with timeout
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            logger.info("SMTP connection established")
            if settings.SMTP_TLS:
                server.starttls()
                logger.info("TLS started")
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                logger.info(f"Logged in as {settings.SMTP_USER}")
            server.send_message(message)
            logger.info("Message sent successfully")

        logger.info(f"Order confirmation email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}", exc_info=True)
        return False


def send_verification_email(email: str, verification_token: str, full_name: Optional[str] = None) -> bool:
    """Send email verification link to new users."""
    subject = "Verify Your Email - Leather Accessories Store"

    name = full_name or email.split('@')[0]
    verification_link = f"http://localhost:4200/verify-email?token={verification_token}"

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #2c1810;
                color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .button {{
                display: inline-block;
                padding: 12px 24px;
                background-color: #d4a574;
                color: white;
                text-decoration: none;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Verify Your Email</h1>
            </div>
            <div class="content">
                <h2>Hello {name}!</h2>
                <p>Thank you for registering with Leather Accessories Store.</p>
                <p>Please click the button below to verify your email address and activate your account:</p>

                <div style="text-align: center;">
                    <a href="{verification_link}" class="button">Verify Email Address</a>
                </div>

                <p>Or copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{verification_link}</p>

                <p>This link will expire in 24 hours.</p>
                <p>If you didn't create an account, you can safely ignore this email.</p>

                <p>Best regards,<br>The Leather Accessories Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 Leather Accessories Store. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return _send_email(email, subject, html_body)


def send_welcome_email(email: str, full_name: Optional[str] = None) -> bool:
    """Send welcome email to verified users."""
    subject = "Welcome to Leather Accessories Store!"

    name = full_name or email.split('@')[0]

    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background-color: #2c1810;
                color: #f5f5f5;
                padding: 20px;
                text-align: center;
            }}
            .content {{
                padding: 20px;
                background-color: #f9f9f9;
            }}
            .footer {{
                text-align: center;
                padding: 20px;
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Leather Accessories Store!</h1>
            </div>
            <div class="content">
                <h2>Hello {name}!</h2>
                <p>Your email has been verified successfully!</p>
                <p>We're excited to have you as part of our community of leather goods enthusiasts.</p>
                <p>Browse our collection of handmade leather accessories and find the perfect piece for you.</p>
                <p>Happy shopping!</p>
                <p>Best regards,<br>The Leather Accessories Team</p>
            </div>
            <div class="footer">
                <p>&copy; 2025 Leather Accessories Store. All rights reserved.</p>
            </div>
        </div>
    </body>
    </html>
    """

    return _send_email(email, subject, html_body)


def _send_email(email: str, subject: str, html_body: str) -> bool:
    """Helper function to send emails."""
    # In development without SMTP configured, just log
    if not settings.SMTP_PASSWORD:
        logger.info(f"[DEV] Email to {email}")
        logger.info(f"Subject: {subject}")
        print(f"\n{'='*60}")
        print(f"📧 EMAIL")
        print(f"{'='*60}")
        print(f"To: {email}")
        print(f"Subject: {subject}")
        print(f"{'='*60}\n")
        return True

    # Send actual email via SMTP
    try:
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = f"Leather Accessories Store <{settings.SMTP_FROM_EMAIL}>"
        message["To"] = email

        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        logger.info(f"Attempting to send email to {email} via {settings.SMTP_HOST}:{settings.SMTP_PORT}")

        # Send email with timeout
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=10) as server:
            logger.info("SMTP connection established")
            if settings.SMTP_TLS:
                server.starttls()
                logger.info("TLS started")
            if settings.SMTP_USER and settings.SMTP_PASSWORD:
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                logger.info(f"Logged in as {settings.SMTP_USER}")
            server.send_message(message)
            logger.info("Message sent successfully")

        logger.info(f"Email sent successfully to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}", exc_info=True)
        return False

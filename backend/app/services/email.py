import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Email configuration
# In production, these should come from environment variables
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "noreply@leatherstore.com"
SENDER_PASSWORD = ""  # Set this in production via environment variables


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
    if not SENDER_PASSWORD:
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
        message["From"] = SENDER_EMAIL
        message["To"] = email

        # Attach HTML body
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(message)

        logger.info(f"Order confirmation email sent to {email}")
        return True

    except Exception as e:
        logger.error(f"Failed to send email to {email}: {str(e)}")
        return False


def send_welcome_email(email: str, full_name: Optional[str] = None) -> bool:
    """Send welcome email to new users."""
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
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Welcome to Leather Accessories Store!</h1>
            </div>
            <div class="content">
                <h2>Hello {name}!</h2>
                <p>Thank you for creating an account with us.</p>
                <p>We're excited to have you as part of our community of leather goods enthusiasts.</p>
                <p>Browse our collection of handmade leather accessories and find the perfect piece for you.</p>
                <p>Happy shopping!</p>
                <p>Best regards,<br>The Leather Accessories Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    # In development, just log
    if not SENDER_PASSWORD:
        logger.info(f"[DEV] Welcome email for {email}")
        print(f"\n📧 WELCOME EMAIL sent to {email}\n")
        return True

    # Production email sending logic would go here
    return True

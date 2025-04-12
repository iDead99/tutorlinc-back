from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    # Generate the verification link
    verification_link = f"http://127.0.0.1:5500/frontend/verify-email.html?token={user.verification_token}"

    # Email subject
    subject = "Verify Your Email Address - TutorLinc"

    # Email body with HTML styling
    message = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: 'Arial', sans-serif;
                background-color: #f9f9f9;
                color: #333;
                margin: 0;
                padding: 0;
            }}
            .email-container {{
                width: 100%;
                background-color: #ffffff;
                margin: 20px auto;
                padding: 20px;
                max-width: 600px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }}
            .header {{
                text-align: center;
                margin-bottom: 20px;
            }}
            .header h1 {{
                color: #007BFF;
                font-size: 24px;
            }}
            .content {{
                font-size: 16px;
                line-height: 1.6;
            }}
            .content p {{
                margin: 10px 0;
            }}
            .cta-button {{
                display: inline-block;
                padding: 12px 20px;
                background-color: #4CAF50;
                color: #ffffff;
                text-decoration: none;
                border-radius: 4px;
                font-size: 16px;
                text-align: center;
                margin-top: 20px;
            }}
            .footer {{
                text-align: center;
                font-size: 14px;
                color: #777;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="email-container">
            <div class="header">
                <h1>Welcome to TutorLinc!</h1>
            </div>
            <div class="content">
                <p>Hello {user.first_name},</p>
                <p>We're excited to have you join us. To complete your account setup, please verify your email by clicking the button below:</p>
                <a href="{verification_link}" class="cta-button">Verify Your Email</a>
                <p>This link is valid for 24 hours. If you did not request this email, you can safely ignore it.</p>
            </div>
            <div class="footer">
                <p>Best regards, <br> The TutorLinc Team</p>
            </div>
        </div>
    </body>
    </html>
    """

    # Send the email
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [user.email],
        fail_silently=False,
        html_message=message  # Specify that the email is in HTML format
    )

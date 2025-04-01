from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_verification_email(user):
    """Regenerate code if expired and send a beautifully formatted email with a background."""

    if not user.is_verification_code_valid():
        user.generate_verification_code()
        user.save()  # Save new code & expiry

    print(f"📧 Preparing to send verification email to: {user.email}")  # Debug print

    subject = "🔐 Verify Your Email - Secure Your Account"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    # HTML Email Body with Background  
    html_message = f"""
    <html>
    <body style="font-family: Arial, sans-serif; text-align: center; background-color: #e3f2fd; padding: 40px;">
        <div style="max-width: 500px; background: white; padding: 25px; border-radius: 10px; 
                    box-shadow: 0px 4px 10px rgba(0,0,0,0.1); margin: auto;">
            <h2 style="color: #007BFF;">🔐 Verify Your Email</h2>
            <p style="font-size: 16px; color: #333;">Hello <strong>{user.first_name}</strong>,</p>
            <p style="font-size: 16px; color: #333;">Use the code below to verify your email and secure your account.</p>
            <p style="font-size: 24px; font-weight: bold; color: #007BFF; background-color: #f1f1f1; 
                      padding: 12px; display: inline-block; border-radius: 8px;">
                {user.verification_code}
            </p>
            <p style="font-size: 14px; color: #666;">This code will expire in <strong>5 minutes</strong>. 
                If you didn’t request this, please ignore this email.</p>
            <hr style="border: none; height: 1px; background-color: #ddd; margin: 20px 0;">
            <p style="font-size: 14px; color: #888;">&copy; 2024 Your Company | All rights reserved.</p>
        </div>
    </body>
    </html>
    """

    text_message = f"""
    Hello {user.first_name},

    Your verification code is: {user.verification_code}
    This code will expire in 5 minutes.

    If you did not request this, please ignore this email.
    """

    email = EmailMultiAlternatives(subject, text_message, from_email, recipient_list)
    email.attach_alternative(html_message, "text/html")  # Attach the HTML version

    try:
        email.send()
        print("✅ Email successfully sent!")  # Debug print
        return True
    except Exception as e:
        print(f"❌ Email sending failed: {e}")  # Debug print
        return False

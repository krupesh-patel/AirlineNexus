import sendgrid
from sendgrid.helpers.mail import Mail

def send_email_sendgrid(subject, body, to_email):
    from_email = "krupeshpatel7898@gmail.com"
    sg = sendgrid.SendGridAPIClient(api_key="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")
    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=body
    )
    try:
        response = sg.send(message)
        print(f"Email sent successfully to {to_email}. Response status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")

# Example usage
send_email_sendgrid(
    subject="Test Email",
    body="This is a test email sent using SendGrid.",
    to_email="krupeshsavaliya700@gmail.com"
)

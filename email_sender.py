import resend
from config import RESEND_API_KEY, FROM_EMAIL, TO_EMAIL

resend.api_key = RESEND_API_KEY

def send_email(subject, html_content):
    try:
        params = {
            "from": FROM_EMAIL,
            "to": TO_EMAIL,
            "subject": subject,
            "html": html_content,
        }

        resend.Emails.send(params)
        print("Email sent successfully to all recipients.")

    except Exception as e:
        print("Error sending email:", e)

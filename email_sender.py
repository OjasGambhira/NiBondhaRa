import resend
from config import RESEND_API_KEY, FROM_EMAIL, TO_EMAILS

resend.api_key = RESEND_API_KEY

def send_email(subject, html_content):
    try:
        for recipient in TO_EMAILS:
            params = {
                "from": FROM_EMAIL,
                "to": recipient,
                "subject": subject,
                "html": html_content,
            }

            resend.Emails.send(params)
            print(f"Email sent successfully to {recipient}")

    except Exception as e:
        print("Error sending email:", e)

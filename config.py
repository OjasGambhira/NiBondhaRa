import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_SECRET_KEY = os.getenv("MAILJET_SECRET_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
FROM_EMAIL = "onboarding@resend.dev"   # works without domain verification
TO_EMAILS = ["gambhiraojas45@gmail.com"]  # List of recipient emails
import os
import requests
import smtplib
from email.mime.text import MIMEText

# Read values from GitHub Secrets (as env variables)
WORKDAY_URL = os.getenv("WORKDAY_URL")
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

# Log values (safe to log because URL is not sensitive)
print(f"🔎 Checking Workday URL: {WORKDAY_URL}")

if not WORKDAY_URL or not TO_EMAIL or not FROM_EMAIL or not GMAIL_APP_PASSWORD:
    print("❌ Missing required environment variables. Check GitHub Secrets.")
    raise Exception("Missing required environment variables.")

def send_email_alert(error_msg):
    print(f"📧 Sending alert email: {error_msg}")

    msg = MIMEText(f"⚠️ Workday might be DOWN.\n\nDetails:\n{error_msg}")
    msg['Subject'] = "ALERT: Workday Down"
    msg['From'] = FROM_EMAIL
    msg['To'] = TO_EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(FROM_EMAIL, GMAIL_APP_PASSWORD)
    server.sendmail(FROM_EMAIL, TO_EMAIL, msg.as_string())
    server.quit()

try:
    response = requests.get(WORKDAY_URL, timeout=10)

    print(f"📡 Received Response Code: {response.status_code}")

    if response.status_code in [200, 302, 404]:
        print("✅ Workday is UP (valid response). No alert sent.")
    else:
        print("⚠️ Workday returned unusual status. Sending alert.")
        send_email_alert(f"HTTP Status Code: {response.status_code}")

except Exception as e:
    print(f"❌ Exception occurred: {str(e)}")
    send_email_alert(str(e))

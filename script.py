# script.py
import os
import re
import time
import smtplib
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
from dotenv import load_dotenv

# --- Load .env ---
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

sender_email = os.getenv("SENDER_EMAIL")
sender_password = os.getenv("SENDER_PASSWORD")
smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
smtp_port = int(os.getenv("SMTP_PORT", "587"))

# --- Debug Print ---
print("Email:", sender_email)
print("SMTP Server:", smtp_server)
print("Password:", "SET" if sender_password else "NOT SET")

# --- File Paths ---
resume_path = "Avantika_Deshmukh_resume_.pdf"
recipients_file = "today2.xlsx"
log_file = "Vemail_log.csv"
email_template_file = "email.html"


# --- Subject ---
subject = "Referral Request – Software Engineer | React | Java "

# --- Load HTML Email Template ---
try:
    with open(email_template_file, "r", encoding="utf-8") as f:
        email_body = f.read()
except FileNotFoundError:
    print("❌ Email template not found! Please create email_template.html")
    exit()



# --- Load Recipients ---
try:
    recipients = pd.read_excel(recipients_file)
except Exception as e:
    print(f"❌ Error reading recipients file: {e}")
    exit()

# --- Load Already Sent Emails ---
if os.path.exists(log_file):
    sent_log = pd.read_csv(log_file)
    already_sent = set(
    sent_log["Email"].astype(str).str.strip().str.lower()
)

else:
    already_sent = set()

hard_bounce_emails = set()

bounce_log_file = "bounce_log.csv"
if os.path.exists(bounce_log_file) and os.path.getsize(bounce_log_file) > 0:
    bounce_df = pd.read_csv(bounce_log_file)
    if "Email" in bounce_df.columns:
        hard_bounce_emails = set(
            bounce_df["Email"].astype(str).str.strip().str.lower()
        )
 

# --- Setup SMTP ---
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
server.login(sender_email, sender_password)

# --- Regex for Email ---
email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")

# --- Initialize Log ---
log_data = []
sent_count = 0
total_count = len(recipients)

# --- Throttle Settings ---
MAX_EMAILS_PER_RUN = 400   # change as per Gmail limits (~300/day)
DELAY_BETWEEN_EMAILS = 15  # seconds delay between emails

# --- Loop Through Recipients ---
for idx, row in recipients.iterrows():
    serial_no = idx + 1
    receiver_email = str(row.get('email')).strip().lower()

    if not receiver_email or not email_pattern.fullmatch(receiver_email):
        print(f"{serial_no}/{total_count} ⚠️ Skipping invalid email: {receiver_email}")
        log_data.append([serial_no, receiver_email, "Invalid Format", datetime.now().strftime("%d-%m-%Y %H:%M:%S")])
        continue

    if receiver_email in hard_bounce_emails:
         print(f"{serial_no}/{total_count} ⛔ Skipping hard bounced email: {receiver_email}")
         log_data.append([
         serial_no,
         receiver_email,
        "Skipped - Hard Bounce",
        datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    ])
         continue

    if receiver_email in already_sent:
        print(f"{serial_no}/{total_count} ⏭️ Skipping {receiver_email} (already sent earlier)")
        continue

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(email_body, 'html'))

    try:
        with open(resume_path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(resume_path)}"')
            msg.attach(part)
    except Exception as e:
        print(f"{serial_no}/{total_count} ❌ Attachment error for {receiver_email} | {e}")
        log_data.append([serial_no, receiver_email, f"Attachment Error: {e}", datetime.now().strftime("%d-%m-%Y %H:%M:%S")])
        continue

    try:
        server.send_message(msg)
        sent_count += 1
        print(f"{serial_no}/{total_count} ✅ Email sent to {receiver_email}")
        log_data.append([serial_no, receiver_email, "Sent", datetime.now().strftime("%d-%m-%Y %H:%M:%S")])
    except Exception as e:
        print(f"{serial_no}/{total_count} ❌ Failed to send to {receiver_email}: {e}")
        log_data.append([serial_no, receiver_email, f"Error: {e}", datetime.now().strftime("%d-%m-%Y %H:%M:%S")])

    # --- Throttle ---
    if sent_count % MAX_EMAILS_PER_RUN == 0:
        print("🚦 Reached max emails for this run. Stopping.")
        break
    time.sleep(DELAY_BETWEEN_EMAILS)

# --- Save Log ---
df_log = pd.DataFrame(log_data, columns=["S.No.", "Email", "Status", "Timestamp"])
if os.path.exists(log_file):
    df_log.to_csv(log_file, mode='a', header=False, index=False)
else:
    df_log.to_csv(log_file, mode='w', header=True, index=False)

print(f"\n📄 Log saved to '{log_file}'")
print(f"✅ Total emails successfully sent: {sent_count}/{total_count}")

# --- Close Server ---
server.quit()



# bounce_reader.py
import imaplib
import email
import re
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("SENDER_EMAIL")
PASSWORD = os.getenv("SENDER_PASSWORD")
IMAP_SERVER = "imap.gmail.com"

bounce_log_file = "bounce_log.csv"

# Connect to mailbox
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL, PASSWORD)
mail.select("inbox")

# Search bounce mails
status, messages = mail.search(None, '(FROM "mailer-daemon" FROM "postmaster")')

email_ids = messages[0].split()
bounce_data = []

for eid in email_ids:
    status, msg_data = mail.fetch(eid, "(RFC822)")
    raw_email = msg_data[0][1]
    msg = email.message_from_bytes(raw_email)

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body += part.get_payload(decode=True).decode(errors="ignore")
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")

    # Detect address-not-found
    if re.search(r'address not found|user unknown|550 5\.1\.1', body, re.I):
        match = re.search(r'Final-Recipient:.*?;\s*(\S+)', body)
        if match:
            failed_email = match.group(1)
            bounce_data.append([
                failed_email,
                "Address Not Found",
                datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            ])

    # Mark mail as seen
    mail.store(eid, '+FLAGS', '\\Seen')

mail.logout()

# Save bounce log
if bounce_data:
    df = pd.DataFrame(bounce_data, columns=["Email", "Status", "Timestamp"])
    if os.path.exists(bounce_log_file):
        df.to_csv(bounce_log_file, mode="a", header=False, index=False)
    else:
        df.to_csv(bounce_log_file, index=False)

print(" Bounce mail processing completed")

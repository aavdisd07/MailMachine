
# HRMailerPro 💼

**HRMailerPro** is a Python automation tool that helps job-seekers (especially freshers) send personalized resume emails in bulk to HRs and recruiters. It supports PDF attachments, tracks delivery status, and includes well-formatted HTML email content with links to your projects and profiles.

---

## 📌 Features

- ✅ Send resume emails with HTML formatting
- ✅ Attach resume PDF file automatically
- ✅ Read recipient emails from Excel file
- ✅ Custom subject and body for each application
- ✅ Track delivery status in a CSV log
- ✅ Supports Gmail with App Password (2-step verification)

---
```
## 📂 Project Structure
📁 HRMailerPro
├── script.py # Main automation script
├── .env # Environment variables (email + app password)
├── recipients.xlsx # Final cleaned list of HR/recruiter emails
├── HR_FINAL_LIST.xlsx # Raw full HR list (if needed)
├── VAIBHAV_LANJEWAR_RESUME.pdf # Attached resume file
├── Vemail_log.csv # Auto-generated mail log
└── README.md # This file
```
---

## ⚙️ Setup Instructions

### 🔸 Step 1: Clone the repo

```bash
git clone https://github.com/Vaibhavlanjewar/HRMailerPro.git
cd HRMailerPro
```

```
###🔸 Step 2: Install dependencies
pip install pandas python-dotenv openpyxl

🔐 Gmail App Password Setup (Required)
If you use Gmail with 2-Step Verification, you must generate an App Password.
https://myaccount.google.com/security
How to create an App Password:
Go to: Google Account - Security

### Enable 2-Step Verification
Scroll to App Passwords
Choose App: Mail and Device: Windows Computer (or any)
Generate → Copy the 16-digit password
```
```
>>Then create your .env file like:
>>SENDER_EMAIL=your_email@gmail.com
>>SENDER_PASSWORD=your_16_digit_app_password
```
```
✉️ Add Recipient Emails
Open HR_FINAL_LIST.xlsx and copy the email column

Paste into recipients.xlsx under the column email

Save it before running the script
```

>>⚠️ Gmail Limits: Stick to <300 emails/day for regular Gmail. Space them out if needed.

Run Script:
```python script.py```



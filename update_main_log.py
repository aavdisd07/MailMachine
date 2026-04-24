# update_main_log.py
import pandas as pd
import os

main_log_file = "Vemail_log.csv"
bounce_log_file = "bounce_log.csv"

# Load logs
main_log = pd.read_csv(main_log_file)
if os.path.exists(bounce_log_file) and os.path.getsize(bounce_log_file) > 0:
    bounce_log = pd.read_csv(bounce_log_file)
else:
    print("ℹ️ No bounce data yet. Nothing to update.")
    exit()


# Get bounced email list
bounced_emails = set(bounce_log["Email"].str.strip().str.lower())

# Update status in main log
main_log.loc[
    main_log["Email"].str.strip().str.lower().isin(bounced_emails),
    "Status"
] = "Hard Bounce - Address Not Found"

# Save updated log
main_log.to_csv(main_log_file, index=False)

print(" Main mail log updated with bounce status")

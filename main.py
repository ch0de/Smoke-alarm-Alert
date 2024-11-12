#Firealarm Monitor and alert
#Mark Brotcke
#1.2.1


import network
import time
import machine
import umail
from machine import Pin
from utime import sleep, localtime, time

# Pin assignment
SMOKE_ALARM_PIN = Pin(4, Pin.IN, Pin.PULL_UP)

# Wi-Fi Credentials
SSID = 'wifi'
PASSWORD = 'password' 

# Email settings
SMTP_SERVER = "SMTP Server"
SMTP_PORT = 465  
SENDER_EMAIL = "from e-mail"
SENDER_PASSWORD = "E-mail password"  # Use an app-specific password for Gmail

# Define email recipients
STARTUP_EMAIL = "start up email address  # Startup email recipient
ALERT_EMAILS = ["email1, email2"]  # Smoke alarm alert recipients

# Email subject and body
SUBJECT_SMOKE_ALARM = "Smoke Alarm Triggered"
BODY_TEMPLATE = """
Hello,

The smoke alarm has been triggered.

Please check the area and take any necessary actions.

Regards,
Raspberry Pi Monitor
"""

# Track the last email time to enforce a 2-minute delay between emails if triggered
LAST_EMAIL_TIME = None
DELAY_AFTER_TRIGGER = 120  # 2 minutes in seconds

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        print("Attempting to connect to Wi-Fi...")
        sleep(1)

    print(f"Connected to Wi-Fi: {wlan.ifconfig()}")

def send_initialization_email():
    subject = "Smoke Alarm Monitoring System Started!"
    body = "Monitoring smoke alarm has started."
    print("Sending system startup email to:", STARTUP_EMAIL)
    send_email(subject, body, [STARTUP_EMAIL])

def main():
    global LAST_EMAIL_TIME

    # Connect to Wi-Fi
    connect_wifi()

    # Send initialization email
    send_initialization_email()

    try:
        while True:
            smoke_alarm_triggered = not SMOKE_ALARM_PIN.value()
#            print("Smoke alarm state checked. Triggered:", smoke_alarm_triggered)

            if smoke_alarm_triggered:
                # Check if 2 minutes have passed since the last email
                if can_send_email(LAST_EMAIL_TIME):
                    print("Smoke alarm triggered. Sending alert email to recipients.")
                    send_email(SUBJECT_SMOKE_ALARM, BODY_TEMPLATE, ALERT_EMAILS)
                    LAST_EMAIL_TIME = time()  # Update the last email time
                    print("Email sent. Waiting for 2 minutes before next check.")
                else:
                    print("Email not sent. 2-minute delay not yet elapsed.")
                
                # Wait for 2 minutes before rechecking
                sleep(DELAY_AFTER_TRIGGER)
            else:
                # Check the pin every 5 seconds if no alarm is triggered
#                print("No alarm triggered. Checking again in 5 seconds.")
                sleep(5)

    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")

def send_email(subject, body, recipients):
    try:
        print(f"Connecting to SMTP server {SMTP_SERVER} on port {SMTP_PORT}.")
        smtp = umail.SMTP(SMTP_SERVER, SMTP_PORT, ssl=True)
        smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
        print("Logged into SMTP server successfully.")

        # Send email to each recipient
        for recipient in recipients:
            print(f"Sending email to {recipient} with subject: '{subject}'")
            smtp.to(recipient)
            smtp.write(f"Subject: {subject}\n")
            smtp.write(f"From:Smoke Alert <{SENDER_EMAIL}>\n")
            smtp.write(f"To: {recipient}\n")
            smtp.write(body)
            smtp.send()
            print(f"Email sent to {recipient}")

        smtp.quit()
        print("Disconnected from SMTP server.")

    except Exception as e:
        print(f"Error sending email: {e}")

def can_send_email(last_email_time):
    # Check if 2 minutes have passed since the last email
    current_time = time()
    time_since_last_email = current_time - last_email_time if last_email_time else None
    print(f"Time since last email: {time_since_last_email} seconds (Delay required: {DELAY_AFTER_TRIGGER} seconds)")
    
    if last_email_time is None:
        print("No previous email sent. Allowing email to be sent.")
        return True
    elif time_since_last_email >= DELAY_AFTER_TRIGGER:
        print("2 minutes have elapsed since last email. Allowing email to be sent.")
        return True
    else:
        print("2 minutes have not yet elapsed. Email will not be sent.")
        return False

if __name__ == "__main__":
    main()



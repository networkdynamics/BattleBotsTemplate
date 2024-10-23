import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email():
    sender_email = os.getenv("SENDER_EMAIL")
    receiver_email = os.getenv("RECEIVER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    session_id = os.getenv('SESSION_ID')


    subject = "Session Results"
    body = f'These are the logs you had for session number {session_id}. Thank for participating!'

    with open("run.log", "rb") as attachment:
        # Add the attachment to the message
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= 'run.log'",
        )

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = receiver_email
    html_part = MIMEText(body)
    message.attach(html_part)
    message.attach(part)

    # Send the email
    with smtplib.SMTP_SSL('Smtp.gmail.com', 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())

if __name__ == "__main__":
    send_email()
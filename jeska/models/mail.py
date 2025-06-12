import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class EmailSender:
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("EMAIL_USER", "jeska.notifications@gmail.com")
        self.app_password = os.getenv("EMAIL_APP_PASSWORD")
        
        if not self.app_password:
            raise ValueError("EMAIL_APP_PASSWORD environment variable is not set")

    def send_email(
        self,
        to_emails: List[str],
        subject: str,
        body: str,
        html_content: Optional[str] = None
    ) -> bool:
        """
        Send an email to one or multiple recipients.
        
        Args:
            to_emails: List of recipient email addresses
            subject: Email subject
            body: Plain text email body
            html_content: Optional HTML content for the email
            
        Returns:
            bool: True if email was sent successfully, False otherwise
        """
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = ", ".join(to_emails)
            msg['Subject'] = subject

            # Add plain text body
            msg.attach(MIMEText(body, 'plain'))

            # Add HTML content if provided
            if html_content:
                msg.attach(MIMEText(html_content, 'html'))

            # Create SMTP connection
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Enable TLS
                server.login(self.sender_email, self.app_password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Failed to send email: {str(e)}")
            return False

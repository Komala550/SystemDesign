import smtplib
import threading
import time
from datetime import datetime, timedelta
from typing import List

class EmailSender:
    def __init__(self, smtp_server: str, port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.username = username
        self.password = password

    def send_email(self, recipient: str, subject: str, message: str):
        try:
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.username, self.password)
                msg = f"Subject: {subject}\n\n{message}"
                server.sendmail(self.username, recipient, msg)
                print(f"Email sent to {recipient}")
        except Exception as e:
            print(f"Error sending email: {e}")

class SMSSender:
    def send_sms(self, phone_number: str, message: str):
        print(f"SMS sent to {phone_number}: {message}")

class PushNotificationSender:
    def send_push_notification(self, device_id: str, message: str):
        print(f"Push notification sent to device {device_id}: {message}")

class NotificationManager:
    def __init__(self):
        self.notifications = []
        self.email_sender = None
        self.sms_sender = SMSSender()
        self.push_sender = PushNotificationSender()
        self.lock = threading.Lock()

    def set_email_sender(self, smtp_server: str, port: int, username: str, password: str):
        self.email_sender = EmailSender(smtp_server, port, username, password)

    def schedule_notification(self, recipient: str, message: str, channel: str, delay_seconds: int):
        send_time = datetime.now() + timedelta(seconds=delay_seconds)
        self.notifications.append((send_time, recipient, message, channel))
        print(f"Notification scheduled for {send_time} on channel {channel}")

    def start(self):
        thread = threading.Thread(target=self._process_notifications)
        thread.daemon = True
        thread.start()

    def _process_notifications(self):
        while True:
            try:
                now = datetime.now()
                with self.lock:
                    for notification in self.notifications[:]:
                        send_time, recipient, message, channel = notification
                        if now >= send_time:
                            self._send_notification(recipient, message, channel)
                            self.notifications.remove(notification)
            except Exception as e:
                print(f"Error processing notifications: {e}")
            time.sleep(1)  # Check every second

    def _send_notification(self, recipient, message, channel):
        if channel == 'email' and self.email_sender:
            self.email_sender.send_email(recipient, "Notification", message)
        elif channel == 'sms':
            self.sms_sender.send_sms(recipient, message)
        elif channel == 'push':
            self.push_sender.send_push_notification(recipient, message)
        else:
            print(f"Unknown channel: {channel}")

def main():
    manager = NotificationManager()
    manager.set_email_sender("smtp.gmail.com", 587, "your_email@gmail.com", "your_password")
    manager.schedule_notification("user@example.com", "This is a test email notification", "email", 10)
    manager.schedule_notification("+1234567890", "This is a test SMS notification", "sms", 15)
    manager.schedule_notification("device123", "This is a test push notification", "push", 20)
    manager.start()

    # Keep the main thread alive to allow background notifications to be processed
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Notification system shutting down.")

if __name__ == "__main__":
    main()

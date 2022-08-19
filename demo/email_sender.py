import sendgrid
import os
from sendgrid.helpers.mail import Mail, Email, To, Content

class EmailSender:
    def __init__(self):
        pass
    def send_email(self, to):
        sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
        from_email = Email("vnajforecast@outlook.com")  # Change to your verified sender
        to_email = To(to)  # Change to your recipient
        subject = "Sending with SendGrid is Fun"
        content = Content("text/plain", "and easy to do anywhere, even with Python. DEMO EMAIL SENDING PRY20220181")
        mail = Mail(from_email, to_email, subject, content)

        # Get a JSON-ready representation of the Mail object
        mail_json = mail.get()

        # Send an HTTP POST request to /mail/send
        response = sg.client.mail.send.post(request_body=mail_json)
        print(response.status_code)
        print(response.headers)


if __name__ == '__main__':
    # print(os.environ.get('SENDGRID_API_KEY'))
    print('This is the EmailSender module for PRY20220181 Reminder Scheduler Lambda')
    email_sender = EmailSender()
    email_sender.send_email("u201810503@upc.edu.pe")
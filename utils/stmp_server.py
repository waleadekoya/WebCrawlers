import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class SendMultipartEmail:

    def __init__(
            self,
            subject: str,
            sender: str,
            recipients: str,
            attachment_body: str
    ):
        self.subject = subject
        self.sender = sender
        self.recipients = recipients
        self.attachment_body = attachment_body
        self.msg = MIMEMultipart()
        self._build_multiparts()
        self.send()

    def send(self):
        with smtplib.SMTP(host=os.getenv('EMAIL_HOST'), port=0) as smtp:  # 'mail.btinternet.com'
            smtp.login(user=os.getenv('EMAIL_ID'), password=os.getenv('EMAIL_PASSWORD'))
            smtp.send_message(self.msg)

    def _build_multiparts(self):
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.sender
        self.msg['To'] = self.recipients
        html_content = f"""\
        <html>
          <head>Job Results for {datetime.now().strftime("%d %b %Y T%H:%M:%S%p")}</head>
          <br>
          <body>
            {self.attachment_body}
          </body>
        </html>
        """
        print(html_content)
        print("test env variables", os.getenv('EMAIL_HOST'))
        self.msg.attach(MIMEText(html_content, 'html'))

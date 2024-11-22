import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from credentials import getPostmanSenderEmail, getPostmanSenderPassword, getPostmanRecipients

class Postman:
    _instance = None

    def __init__(self) -> None:
        raise RuntimeError('Postman needs to be used as a singleton. Call get_singleton() instead!')
    
    @classmethod
    def get_singleton(cls):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            cls.__init_singleton(cls)
        return cls._instance
    
    def __init_singleton(self):
        self.port = 465
        self.smtp_server = "smtp.gmail.com"
        self.sender_email = getPostmanSenderEmail()
        self.password = getPostmanSenderPassword()
        self.recipients = getPostmanRecipients()
        self.send_email(self, 'kg8Xszb4iTradingBot started running', 'kg8Xszb4iTradingBot started running')

    def send_email(self, subject, body):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = ', '.join(self.recipients)
        msg["Subject"] = subject
        body = MIMEText(body)
        msg.attach(body)
        
        server = smtplib.SMTP_SSL(self.smtp_server, self.port)

        server.login(self.sender_email, self.password)
        server.sendmail(self.sender_email, self.recipients, msg.as_string())
        server.quit()

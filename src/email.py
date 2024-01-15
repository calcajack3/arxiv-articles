from jinja2 import Environment, FileSystemLoader
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

class Email:
    def __init__(self):
        self.template_file = 'articles.html'
        self.template = None
        self.output = None
        load_dotenv()
        self.email = os.getenv('EMAIL')
        self.password = os.getenv('EMAIL_PASS')


    def load_template(self):
        env = Environment(loader=FileSystemLoader('src/templates/'))
        self.template = env.get_template(self.template_file)

    def render(self, data):
        return self.template.render(data)

    def prepare_email(self, articles, n_selected_articles):
        date = datetime.now().strftime("%B %d")
        data = {
            'date': date,
            'n_selected_articles': n_selected_articles,
            'articles': articles
        }
        self.load_template()
        output = self.render(data)
        self.output = output
        with open('src/templates/email.html', 'w') as f:
            f.write(self.output)
        print(output)

    def send_email(self, recipient_email):
        """
        Sends the email using smtplib and email.mime
        :param sender_email: The email address to send from.
        :param password: The password for the sender's email account.
        :param recipient_email: The email address to send to.
        """
        # Set up the SMTP server
        server = smtplib.SMTP('smtp-mail.outlook.com', 587)
        server.ehlo("outlook")
        server.starttls()
        server.ehlo("outlook")
        server.login(self.email, self.password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient_email
        msg['Subject'] = "Your Daily Arxiv Articles Digest"

        # Attach the HTML content
        msg.attach(MIMEText(self.output, 'html'))

        # Send the email and close the server
        server.send_message(msg)
        server.quit()
        print("Email sent successfully to", recipient_email)
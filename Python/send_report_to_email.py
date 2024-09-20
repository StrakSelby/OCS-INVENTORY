import os 
# smtplib provides functionality to send emails using SMTP.
import smtplib
# MIMEMultipart send emails with both text content and attachments.
from email.mime.multipart import MIMEMultipart
# MIMEText for creating body of the email message.
from email.mime.text import MIMEText
# MIMEApplication attaching application-specific data (like CSV files) to email messages.
from email.mime.application import MIMEApplication

subject = 'Inventory Report'
body = 'Testing report sending using email'
sender_email = ''
reciever_email = ''
sender_password = '' #app password need 2 factors authentication to make one 
smtp_server = 'smtp.gmail.com'
smtp_port = 465
path_to_directory = '/home/vannaboth/OCS-INVENTORY/Python/pdf_output'

# MIMEMultipart() creates a container for an email message that can hold
message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = reciever_email
body_part = MIMEText(body)
message.attach(body_part)

for filename in os.listdir(path_to_directory):
        if filename.endswith('.pdf'):
           file_path = os.path.join(path_to_directory, filename)
           with open(file_path,'rb') as file:
                message.attach(MIMEApplication(file.read(), Name=filename))

with smtplib.SMTP_SSL(smtp_server,smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email,reciever_email, message.as_string())

print('Sucessfully send the report to the email')
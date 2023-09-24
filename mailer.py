from email.message import EmailMessage
import ssl
import smtplib
def sendem(name):
    email_sender='ieeedemo754@gmail.com'
    email_password=''
    email_receiver=''
    subject='Request for connection to client name: '+name
    body="""pls connect on the required google link\n"""
    print(body)
    em=EmailMessage()
    em['From']=email_sender
    em['To']=email_receiver
    em['subject']=subject
    em.set_content(body)
    context=ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context) as smtp:
        smtp.login(email_sender,email_password)
        smtp.sendmail(email_sender,email_receiver,em.as_string())

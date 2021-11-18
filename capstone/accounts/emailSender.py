
from django.core.mail import BadHeaderError, EmailMessage
from django.template.loader import render_to_string
from accounts.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator

def emailSender(request, model):

    subject, from_email, to = 'hello', 'from@example.com', 'to@example.com'
    html_content = render_to_string( 'email.html', {'model':model, 'sender':request.user})
    msg = EmailMessage(subject, html_content, from_email, [to])
    msg.content_subtype = "html"  # Main content is now text/html
    msg.send()
    #PasswordResetTokenGenerator.
    return 0






# By default, the MIME type of the body parameter in an EmailMessage is "text/plain". It is good practice to leave this alone, 
# because it guarantees that any recipient will be able to read the email, regardless of their mail client. However, 
# if you are confident that your recipients can handle an alternative content type, 
# you can use the content_subtype attribute on the EmailMessage class to change the main content type. 
# The major type will always be "text", but you can change the subtype. For example:

# msg = EmailMessage(subject, html_content, from_email, [to])
# msg.content_subtype = "html"  # Main content is now text/html
# msg.send()

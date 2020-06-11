import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.conf import settings
class Outbound:
    @staticmethod
    def send_email(request, message):
        port = 25
        with smtplib.SMTP('localhost') as server:
            server.sendmail("vortexrentalshop@gmail.com", str(request), message.as_string())

    @staticmethod
    def sendSignUpConfirmation(request, to_username, to_user_email):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Account for Vortex Rentals succesfully Created"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "You"
        html = """<html><body><h2>Account has been created!</h2><h4> <br/>
                We look forward to your business .<br/> Thank you!!!<br/> 
                  Account Name: {}</h4></body></html>""".format(to_username)
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(to_user_email, message)
    
    @staticmethod
    def sendRenatlConfirmation(request, to_new_rental):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Account for Vortex Rentals succesfully Created"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "You"
        html = """<html><body><h2>Server has been created!</h2><h4> <br/>
                We look forward to future business {0}.<br/> Thank you!!!<br/> 
                 {1}</h4></body></html>""".format(request.user.username,to_new_rental)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendTicketCreateConfirmation(request,title):
        message = MIMEMultipart("alternative")
        message["Subject"] = "You have Succesfully Created a Ticket"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "You"
        html = """<html><body><h2>A staff memeber will deal with your issue when avaible!</h2><h4> <br/>
                We hope to have the ticket dealt within 3-5 days {0}.<br/><br/> 
                 Ticket Name: {1}</h4></body></html>""".format(request.user.username, title)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)

    @staticmethod
    def sendTicketClosedConfirmation(request,ticket):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Ticket has been closed"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your Ticket has been Closed"
        html = """<html><body><h2>Hi {0}. Your Ticket was resolved by {1}[staff]</h2><h4> <br/>
                We hope to have resolved the issue that you had!.<br/><br/> 
                 Ticket Name: {2}</h4></body></html>""".format(ticket.author ,request.user.username, ticket.title)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendTicketRefundConfirmation(request, ticket):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your order has been refunded"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your Ticket has been refunded"
        html = """<html><body><h4>Hi {0}. Your Ticket was refunded by {1}[staff]
        <br/>You should recieve the money back within 3-5 days .<br/><br/> 
                 Ticket Name: {2}</h4></body></html>""".format(request.user.username, ticket.author ,ticket.title)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
		
    
    @staticmethod
    def sendEditProfilePassword(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Profile details have been updated"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your Passowrd has been Updated"
        html = """<html><body><h2>Hi {0}. Your Password has beden changed</h2><h4> <br/>
                </h4></body></html>""".format(request.user.username)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendEditProfile(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Profile details have been updated"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your Profile details have been updated"
        html = """<html><body><h2>Hi {0}. Your Profile details has been updated</h2><h4> <br/>
                </h4></body></html>""".format(request.user.username)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendEditProfileCard(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your Profile details have been updated"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your Profile Card details have been updated"
        html = """<html><body><h2>Hi {0}. Your Profile's Card details has been updated</h2><h4> <br/>
                </h4></body></html>""".format(request.user.username)
        
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendRenatalExpiry(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your rental server has expired"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your rental server has expired"
        html = """<html><body>Hi{}. Your rental server has expired!</h2><h4> <br/>
                We thank you for your business .<br/> Thank you!!!<br/> 
                  </h4></body></html>""".format(request.user.username)
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendRenatalExtension(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your rental server has been extended"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your rental server has been extended"
        html = """<html><body>Hi{}. Your rental server has been extended!</h2><h4> <br/>
                We thank you for your business .<br/> Thank you!!!<br/> 
                  </h4></body></html>""".format(request.user.username)
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
    
    @staticmethod
    def sendSharingServer(request):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Your server has been shared"
        message["From"] = "vortexrentalshop@gmail.com"
        message["To"] = "Your rental server has been shared"
        html = """<html><body>Hi{}. Your rental server has been shared!</h2><h4> <br/>
                <br/> Thank you!!!<br/> 
                  </h4></body></html>""".format(request.user.username)
        content = MIMEText(html, "html")
        message.attach(content)
        Outbound.send_email(request.user.email, message)
 



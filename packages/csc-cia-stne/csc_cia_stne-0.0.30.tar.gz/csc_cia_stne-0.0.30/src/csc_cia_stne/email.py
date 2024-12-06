import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pydantic import BaseModel, ValidationError, field_validator

class InitParamsValidator(BaseModel):
    email_sender: str
    email_password: str

    @field_validator('email_sender','email_password')
    def check_str_input(cls, value, info):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"O campo '{info.field_name}' deve ser strings e não {type(value)}")
        return value
    
class SendEmailParamsValidator(BaseModel):

    to: list
    message: str
    title: str
    reply_to:str
    attachments: list = []
    cc: list = []
    cco: list = []

    @field_validator('message','title','reply_to')
    def check_str_input(cls, value, info):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"O campo '{info.field_name}' deve ser strings e não {type(value)}")
        return value
    
    @field_validator('to','attachments','cc','cco')
    def check_list_input(cls, value, info):
        if not isinstance(value, list):
            raise ValueError(f"O parametro '{info.field_name}' deve ser uma lista")
        
        return value

class Email():

    def __init__(self, email_sender, email_password):

        self.email_sender = email_sender
        self.email_password = email_password

        try:
        
            InitParamsValidator(email_sender=email_sender, email_password=email_password)

        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados de input da inicialização da instância:", e.errors())


        self.server = self.login_email()

        if not isinstance(self.server, smtplib.SMTP) and 'status' in self.server and not self.server['status']:

            raise ValueError("Erro na validação dos dados de input da inicialização da instância:", self.server['error'])


    def login_email(self):

        try:

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(self.email_sender, self.email_password)

            return server

        except Exception as e:

            return {
                'status':False,
                'error':str(e)
            }

    
    def send_email( self, to : list , message : str , title : str , reply_to: str, attachments : list = [] , cc : list = [] , cco : list = [] ) -> dict:

        try:
        
            SendEmailParamsValidator(to=to, message=message, title=title, reply_to=reply_to, attachments=attachments, cc=cc, cco=cco)

        except ValidationError as e:
        
            raise ValueError("Erro na validação dos dados para o envio do email:", e.errors())

        try:

            msg = MIMEMultipart()
            
            msg["From"] = self.email_sender
            
            msg["To"] = (",").join(to)
            
            msg["cc"] = (",").join(cc)
            
            msg['Reply-To'] = reply_to

            msg["Subject"] = title

            for file in attachments:

                try:

                    attachment = open(file, "rb")
                    
                    part = MIMEBase("application", "octet-stream")
                    
                    part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    
                    part.add_header("Content-Disposition", f"attachment; filename={file.split('/')[-1]}")
                    
                    msg.attach(part)

                    attachment.close()

                except Exception as e:

                    return {
                        'status':False,
                        'error':str(e)
                    }

            msg.attach(MIMEText(message, 'html'))

            self.server.sendmail(self.email_sender, to + cc + cco, msg.as_string())

            return True

        except Exception as e:

            return {
                'status':False,
                'error':str(e)
            }
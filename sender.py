import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser
import sys, getopt, os
from colorama import Fore
from colorama import Style
from colorama import init

try:
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
except:
  pass

class sender:
    def __init__(self,reception):
        self.config = configparser.ConfigParser(interpolation=None)
        self.config.read('config.txt')
        self.smtp_server = self.config.get("SMTP", "smtp_server")
        self.smtp_port = self.config.get("SMTP", "smtp_port")
        self.smtp_email = self.config.get("SMTP", "smtp_username")
        self.smtp_password = self.config.get("SMTP", "smtp_passowrd")
        self.subject = self.config.get("subject", "subject")
        self.letter = open('letter.txt','rb').read()
        self.color_green = Fore.GREEN + Style.BRIGHT
        self.color_red = Fore.RED + Style.BRIGHT


    def SendMsg(self):
        print(f' [+] Start Send Msg For {reception}')
        msg = MIMEMultipart()
        msg.attach(MIMEText(self.letter,'html','utf-8'))
        FromAdd = f'<{self.smtp_email}>'
        msg['From'] = FromAdd
        msg['To'] =  reception
        msg['Subject'] = self.subject

        try:
            smtp = smtplib.SMTP(self.smtp_server,int(self.smtp_port))
            smtp.ehlo()
            try:
                smtp.starttls()
            except:
                pass
            smtp.login(self.smtp_email,self.smtp_password)
            smtp.sendmail(self.smtp_email, reception, msg.as_string())
            smtp.quit()
            

        
        except smtplib.SMTPException as smtp_srror:
            print(f'{self.color_red} [-] Some Error => {smtp_srror}')
            sys.exit()

        except Exception as error:
            print(f'{self.color_red} [-] Error: Failed Please check readme.txt file\n Error Info => {error}')
            sys.exit()






def usage():
    print('Usage: sender.py -r|--reception reception@email.com')



if __name__ == "__main__":
    reception = None
    argv = sys.argv[1:]
    try:      
        opts, args = getopt.getopt(argv, "r:h:", ['reception=','help='])
    except getopt.GetoptError as error:
        usage()
        sys.exit()  
    if not opts:
        usage()
        sys.exit()
    for opt, arg in  opts:
        if opt in ['-r','--reception']:
            reception = arg
            sender(reception).SendMsg()
        elif opt in ['-h', '--help']:
            usage()
            sys.exit()
        else:
            usage()
            sys.exit()

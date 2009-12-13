#!/usr/bin/python
# encoding: utf-8

import smtplib, datetime, os, tarfile
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from optparse import OptionParser


class Email():
    sender=None
    recipient=None
    
    subject_line="[Gmailer] Automatic backup"
    body="This is an automated backup sent on %s." % str(datetime.date.today())
    attachments=[]
    
    # obviously, do override these properties
    smtp_user=None
    smtp_pass=None
    
    #override these values if you want to use another service
    smtp_server="smtp.gmail.com"
    smtp_port=587
    
    """docstring for ClassName"""
    def __init__(self):
        pass
    
    def construct_message(self):
        msg = MIMEMultipart()

        msg['From'] = self.sender
        msg['To'] = self.recipient
        msg['Subject'] = self.subject_line

        msg.attach(MIMEText(self.body))
        
        for i in self.attachments:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(open(i, 'rb').read())
            Encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                    'attachment; filename="%s"' % os.path.basename(i))
            msg.attach(part)
        
        return msg.as_string()
        
    def check_all_arguments(self):
        REQUIRED=[self.smtp_user, self.smtp_pass]
        
        if self.sender==None:
            self.sender="%s@gmail.com"%self.smtp_user
            self.recipient=self.sender
        
        for i in REQUIRED:
            if (i==None):
                print "You have not set all the properties required for an email."
                print "Please set smtp_user and smtp_pass and try again."
                return False
        return True
    
    def send(self):
        if (self.check_all_arguments()):
            message=self.construct_message()
            # send the mail
            
            mailServer = smtplib.SMTP(self.smtp_server, self.smtp_port)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(self.smtp_user, self.smtp_pass)
            mailServer.sendmail(self.sender, self.recipient, message)
            # Should be mailServer.quit(), but that crashes...
            mailServer.close()

def main():
    """docstring for main"""
    
    parser = OptionParser()
    parser.add_option("-a", "--attachment", dest="attachment",
                      help="Add an attachment to the email", metavar="FILE")
    
    parser.add_option("-u", "--user", dest="user",
                      help="SMTP username (or your GMail username)", metavar="USER")
                      
    parser.add_option("-p", "--pass", dest="passwd",
                      help="SMTP password (or your GMail password)", metavar="PASS")
    
    (options, args) = parser.parse_args()

    tar = tarfile.open("gmailer-backup%s.tar.gz"%str(datetime.date.today()), "w:gz")

    namelist=["/Users/lenni/httpd.conf"]
    for name in namelist:
        tarinfo = tar.gettarinfo(name, "fakeproj-1.0/" + name)
        tarinfo.uid = 123
        tarinfo.gid = 456
        tarinfo.uname = "johndoe"
        tarinfo.gname = "fake"
        tar.addfile(tarinfo, file(name))
    tar.close()
    
    mail=Email()
    mail.smtp_user=options.user
    mail.smtp_pass=options.passwd
    mail.attachments.append(options.attachment)
    mail.send()
    print "Email sent to %s" % mail.recipient

if __name__ == '__main__':
    main()
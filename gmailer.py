#!/usr/bin/python
# encoding: utf-8
import smtplib, sys, MimeWriter, StringIO, base64, mimetypes, datetime

print sys.argv


files=sys.argv
files=files[1:]

class Email():
    """docstring for ClassName"""
    def __init__(self):
        self.sender=None
        self.recipient=None
        
        self.subject_line="[Gmailer] automatic backup"
        self.body="This is an automated backup sent on %s" % str(datetime.date.today())
        self.attachments=[]
        
        #override these values if you want to use another service
        self.smtp_server="smtp.gmail.com"
        self.smtp_port=587
        
        self.smtp_user=None
        self.smtp_pass=None
    
    def construct_message(self):
        message = StringIO.StringIO()
        writer = MimeWriter.MimeWriter(message)
        writer.addheader('Subject', self.subject_line)
        writer.startmultipartbody('mixed')

        # start off with a text/plain part
        part = writer.nextpart()
        body = part.startbody('text/plain')
        body.write(text)

        # now add an attachment
        for i in self.attachments:
			part = writer.nextpart()
			part.addheader('Content-Transfer-Encoding', 'base64')
			part.addheader('Content-disposition:', 'attachment; filename="'+i+'"')
			mtype=mimetypes.guess_type(i)
			mtype=mtype[0]
			if i.endswith('gpg')==True:
				mtype='application/pgp'			
			
			
			print "added attachment: "+i+" ("+mtype+")"
			body = part.startbody(mtype)
			base64.encode(open(i, 'rb'), body)

        # finish off
        writer.lastpart()
        
        return writer.getvalue()
    
    def check_all_arguments(self):
        REQUIRED=[this.sender, this.recipent, this.smtp_user, this.smtp_pass]
        
        for i in REQUIRED:
            if (i==None):
                print "You have not set all the properties required for an email."
                print "Please set sender, recipient, stmp_user and smtp_pass and try again."
                return False
        return True
    
    def send(self):
        if (check_all_arguments()):
            message=this.construct_message()
            # send the mail
            
            mailServer = smtplib.SMTP(self.smtp_server, self.smtp_port)
            mailServer.ehlo()
            mailServer.starttls()
            mailServer.ehlo()
            mailServer.login(self.smtp_user, self.smtp_pass)
            mailServer.sendmail(gmail_user, to, msg.as_string())
            # Should be mailServer.quit(), but that crashes...
            mailServer.close()

def main():
    """docstring for main"""
    mail=Email()

if __name__ == '__main__':
    main()


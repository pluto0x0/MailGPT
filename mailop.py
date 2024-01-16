from utils import Config, Email, find_first_email
import smtplib
from email.mime.text import MIMEText
from typing import List
import imaplib
import email
from email.header import decode_header

class MailOp:
    def __init__(self, config: Config):
        self.cfg = config
    
    def send_email(self, receivers: List[str], subject: str, content: str):
        mail_user = self.cfg.smtp_email.split('@')[0]
        if isinstance(receivers, str):
            receivers = list(map(find_first_email, map(str.strip, receivers.split(','))))
        try:
            # establish SMTP connection
            server = smtplib.SMTP(self.cfg.smtp_server, self.cfg.smtp_port)
            server.ehlo()
            server.starttls()  # enable TLS
            server.ehlo()
            server.login(self.cfg.smtp_email, self.cfg.smtp_password)
            # send email
            email_text = f"From: {self.cfg.smtp_email}\nTo: {','.join(receivers)}\nSubject: {subject}\n\n{content}"
            server.sendmail(self.cfg.smtp_email, receivers, email_text)
            # close connection
            server.quit()
            return {'status': 'success', 'msg': ''}

        except smtplib.SMTPException as e:
            print('error in sending email:', e)  # print errors
            return {'status': 'error', 'msg': repr(e)}

    def receive_last_email(self):

        def get_msg_content(msg):
            if msg.is_multipart():
                # multipart message
                for part in msg.walk():
                    content_type = part.get_content_type()
                    content_disposition = str(part.get("Content-Disposition"))
                    # get text components
                    if content_type == "text/plain" and "attachment" not in content_disposition:
                        return "text/plain", part.get_payload(decode=True).decode(part.get_content_charset())
                    elif content_type == "text/html" and "attachment" not in content_disposition:
                        return "text/html", part.get_payload(decode=True).decode(part.get_content_charset())
            else:
                # not multipart
                return msg.get_content_type(), msg.get_payload(decode=True).decode(msg.get_content_charset())

            return ""

        def decode_mime_words(s):
            decoded_words = decode_header(s)
            return ''.join(word.decode(charset or 'utf-8') for word, charset in decoded_words)
        
        # establish IMAP connection
        mail = imaplib.IMAP4_SSL(self.cfg.imap_server, self.cfg.imap_port)
        mail.login(self.cfg.imap_email, self.cfg.imap_password)
        mail.select('inbox')  # choose "INBOX"

        # search for all unseen emails
        status, messages = mail.search(None, 'UNSEEN')
        status, messages = mail.search(None, 'ALL')
        if status != 'OK':
            print("No new emails to read.")
            # close connection
            mail.close()
            mail.logout()
        else:
            # all 
            num = messages[0].split()[-1]
            status, data = mail.fetch(num, '(RFC822)')
            if status != 'OK':
                return f'error status={status}'
            # get email content
            msg = email.message_from_bytes(data[0][1])
            subject = decode_header(msg["Subject"])[0][0]
            if isinstance(subject, bytes):
                subject = subject.decode(encoding='utf-8')
            from_ = decode_mime_words(msg.get("From"))
            content_type, content = get_msg_content(msg)
            # close connection
            mail.close()
            mail.logout()

            return Email(
                from_=from_,
                to=self.cfg.imap_email,
                subject=subject,
                body=content,
                type_=content_type,
            )

    def __repr__(self):
        return \
f'''
Mail Operations for:{repr(self.cfg)}
'''
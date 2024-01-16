import configparser

class Config:
    def __init__(self, filename='config.ini'): 
        config = configparser.ConfigParser()
        config.read(filename)

        self.smtp_server = config['SMTP']['server']
        self.smtp_port = int(config['SMTP']['port'])
        self.smtp_email = config['SMTP']['email']
        self.smtp_password = config['SMTP']['password']

        self.imap_server = config['IMAP']['server']
        self.imap_port = int(config['IMAP']['port'])
        self.imap_email = config['IMAP']['email']\
                             if 'email' in config['IMAP']\
                             else self.smtp_email
        self.imap_password = config['IMAP']['password']\
                             if 'password' in config['IMAP']\
                             else self.smtp_password
        self.openai_key = config['OpenAI']['key']
        self.openai_model = config['OpenAI']['model']
        self.openai_msg = config['OpenAI']['messages']
        self.openai_func = config['OpenAI']['functions']

    def __repr__(self):
        return \
f'''
SMTP Server:   {self.smtp_server}
SMTP Port:     {self.smtp_port}
SMTP Email:    {self.smtp_email}
IMAP Server:   {self.imap_server}
IMAP Port:     {self.imap_port}
IMAP Username: {self.imap_email}

OpenAI Key:    {self.openai_key}
OpenAI Model:  {self.openai_model}
OpenAI Message JSON:    {self.openai_msg}
OpenAI Function JSON:   {self.openai_func}
'''

class Email:
    def __init__(self, from_:str, to:str, subject:str, body:str, type_:str = 'text/plain'): 
        self.from_ = from_
        self.to = to
        self.subject = subject
        self.body = body
        self.type_ = type_
    
    def __repr__(self):
        def squeeze(s : str, maxlen: int = 1500):
            if len(s) < maxlen:
                return s
            return s[:maxlen] + '...'
        return \
f'''
From:       {self.from_}
To:         {self.to}
Subject:    {self.subject}
Type:       {self.type_}
Body:       {squeeze(self.body)}
'''

import re

def find_first_email(text: str):
    email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_regex, text)
    return emails[0] if emails else None
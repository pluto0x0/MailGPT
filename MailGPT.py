from utils import Config, Email
from mailop import MailOp
from openai_api import OpenAI_api
import json
from pprint import pprint

def send(mailop: MailOp, mail: str):
    if '```json' in mail:
        mail = mail.replace('```json', '')
        mail = mail.replace('```', '')
    try:
        json_mail = json.loads(mail)
    except json.decoder.JSONDecodeError:
        return

    print('\n=== Sending Email ===')
    pprint(json_mail)
    while True:
        res = input('I want to send an email. Proceed? [y/n]: ').strip().lower()
        if res == 'n':
            print('Abort.')
            return
        elif res == 'y':
            break
        else:
            print('Enter again:')
    
    mailop.send_email(json_mail['To'], json_mail['Subject'], json_mail['Body'])
    
if __name__ == '__main__':
    cfg = Config()
    # print(cfg.imap_password)
    mailop = MailOp(cfg)
    # print(mailop)
    # print(cfg)
    # mail.send_email(['zfaye@qq.com'], 'subject', 'hi!')

    print('=== Reading latest email: ===')
    new_mail = mailop.receive_last_email()
    print(new_mail)
    gpt = OpenAI_api(cfg, mailop)
    while True:
        res = input('Proceed? [y/n]: ').strip().lower()
        if res == 'n':
            print('Abort.')
            break
        elif res == 'y':
            res = gpt.run_conversation(new_mail)
            print(f'\n=== ChatGPT [{cfg.openai_model}] Response ===')
            print(res.content)
            send(mailop, res.content)
            break
        else:
            print('Enter again.')
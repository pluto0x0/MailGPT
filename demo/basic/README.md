# MailGPT Demo: Basic

## Intro

This is a basic demo to show how MailGPT works.

## Payload

See [email payload](./payload.txt) sent to MailGPT.

And [MailGPT's response](./response.txt).

## Processes

MailGPT do the following processes:

- Connect to SMTP 
- Fetch the latest email in the inbox
- Feed email to ChatGPT via OpenAI api
- ChatGPT yields a JSON object that contains the information of the email to send
- Send email via IMAP hosts

## Trace

```plaintext
$ python .\MailGPT.py
=== Reading latest email: ===

From:       "zfaye" <zfaye@qq.com>
To:         yzzzf0@gmail.com
Subject:    Can you help me with this question?
Type:       text/plain
Body:       Hi,


Do you know which team won 2018 FIFA World Cup?


Regards,
Zifan

Proceed? [y/n]: y

=== ChatGPT [gpt-4-1106-preview] Response ===
{
  "To": "zfaye@qq.com",
  "Subject": "2018 FIFA World Cup Champions",
  "Body": "Hi Zifan,\n\nThe team that won the 2018 FIFA World Cup in Russia was France. They claimed the title after defeating Croatia 4-2 in the final.\n\nBest regards,\nMailGPT"
}

=== Sending Email ===
{'Body': 'Hi Zifan,\n'
         '\n'
         'The team that won the 2018 FIFA World Cup in Russia was France. They '
         'claimed the title after defeating Croatia 4-2 in the final.\n'
         '\n'
         'Best regards,\n'
         'MailGPT',
 'Subject': '2018 FIFA World Cup Champions',
 'To': 'zfaye@qq.com'}
I want to send an email. Proceed? [y/n]: y
```

# def fetch_emails():
#     return [{"from": "alice@example.com", "subject": "Project Update", "body": "Here’s what we’ve done..."}]

# def send_email_reply(email_id: str, content: str):
#     return {"status": "sent", "email_id": email_id, "reply": content}

# from gmail.gmail_service import get_gmail_service
from gmail.gmail_emailsservice import fetch_unread_emails
import email
from email.header import decode_header
import imaplib

# def read_unread_emails(limit=5):
#     service = get_gmail_service()
#     results = service.users().messages().list(userId='me', labelIds=['INBOX'], q="is:unread").execute()
#     messages = results.get('messages', [])

#     email_list = []
#     for msg in messages[:limit]:
#         msg_data = service.users().messages().get(userId='me', id=msg['id']).execute()
#         snippet = msg_data.get('snippet', '')
#         headers = msg_data.get('payload', {}).get('headers', [])
#         subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
#         sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown Sender)')
        
#         email_list.append({
#             'sender': sender,
#             'subject': subject,
#             'snippet': snippet
#         })

#     return email_list


# Function to fetch unread emails


def fetch_unread_emails():
    # Setup IMAP connection
    # imap_server = "imap.gmail.com"  # Example for Gmail
    # email_user = "komanduri.gopik@gmail.com"
    # email_password = "penfish336"

    # mail = imaplib.IMAP4_SSL(imap_server)
    # mail.login(email_user, email_password)
    # mail.select("inbox")

    # # Search for all unread emails
    # status, messages = mail.search(None, 'UNSEEN')

    # # Fetch email data
    # email_ids = messages[0].split()
    # emails = []

    # for email_id in email_ids:
    #     _, msg_data = mail.fetch(email_id, "(RFC822)")
    #     for response_part in msg_data:
    #         if isinstance(response_part, tuple):
    #             msg = email.message_from_bytes(response_part[1])
    #             subject, encoding = decode_header(msg["Subject"])[0]
    #             if isinstance(subject, bytes):
    #                 subject = subject.decode(encoding if encoding else 'utf-8')
    #             emails.append(subject)

    # mail.logout()
    emails = fetch_unread_emails()
    return emails

print(fetch_unread_emails())

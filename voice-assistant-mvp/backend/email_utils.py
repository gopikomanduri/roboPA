import base64
import json
import re
from gmail.gmail_service import get_gmail_service
from voice_handler import speak, listen
from transformers import pipeline
from email import message_from_bytes

#zero_shot = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

zero_shot = pipeline("zero-shot-classification", model="valhalla/distilbart-mnli-12-1")


CATEGORIES = ["important", "sensitive", "personal", "newsletter", "promotion"]
KEYWORDS = ["jyoti", "asba", "hdfc", "offer", "invoice"]
SUMMARY_FILE = "email_summary.json"

def clean_text(text):
    return re.sub(r'\s+', ' ', text or "").strip().lower()

def decode_email(msg_payload):
    try:
        return base64.urlsafe_b64decode(msg_payload.encode('ASCII'))
    except:
        return None

def classify_email(text):
    result = zero_shot(text, CATEGORIES)
    top_label = result["labels"][0]
    return top_label

def process_unread_emails():
    service = get_gmail_service()

    # Get unread emails
    results = service.users().messages().list(userId='me', labelIds=['INBOX', 'UNREAD'], maxResults=20).execute()
    messages = results.get('messages', [])

    if not messages:
        speak("You have no unread emails.")
        return

    emails = []
    speak(f"You have {len(messages)} unread emails.")

    for msg in messages:
        msg_data = service.users().messages().get(userId='me', id=msg['id'], format='raw').execute()
        raw_msg = decode_email(msg_data['raw'])
        if not raw_msg:
            continue

        mime_msg = message_from_bytes(raw_msg)
        subject = mime_msg.get('Subject', '')
        from_email = mime_msg.get('From', '')
        in_reply_to = mime_msg.get('In-Reply-To', '')
        body = ""

        if mime_msg.is_multipart():
            for part in mime_msg.walk():
                if part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True).decode(errors='ignore')
                    break
        else:
            body = mime_msg.get_payload(decode=True).decode(errors='ignore')

        text = clean_text(subject + " " + body)
        label = classify_email(text)

        email_obj = {
            "id": msg['id'],
            "subject": subject,
            "from": from_email,
            "body": body,
            "reply": bool(in_reply_to),
            "label": label
        }

        emails.append(email_obj)

    # Categorization
    important = [e for e in emails if e["label"] in ["important", "sensitive"] or any(k in e["subject"].lower() for k in KEYWORDS)]
    replies = [e for e in emails if e["reply"]]
    others = [e for e in emails if e not in important and e not in replies]

    speak(f"{len(important)} look important or sensitive, {len(replies)} are replies, and {len(others)} are general emails.")

    # Ask for keyword filter
    speak("Would you like to filter by a specific keyword?")
    response = listen()
    if "yes" in response.lower():
        speak("Please tell me the keyword to search for.")
        keyword = listen().strip().lower()
        filtered = [e for e in emails if keyword in e["subject"].lower() or keyword in e["body"].lower()]
        speak(f"I found {len(filtered)} emails related to {keyword}. Should I read them?")
        if "yes" in listen().lower():
            read_and_mark(filtered, service)
    else:
        speak("Should I read all important emails?")
        if "yes" in listen().lower():
            read_and_mark(important, service)

    # Save summary to JSON
    with open(SUMMARY_FILE, "w") as f:
        json.dump(emails, f, indent=2)
    speak("Email summaries have been saved.")

def read_and_mark(emails, service):
    for email in emails:
        speak(f"From: {email['from']}")
        speak(f"Subject: {email['subject']}")
        speak(f"Body: {email['body'][:300]}")  # limit to 300 chars
        # Mark as read
        service.users().messages().modify(userId='me', id=email['id'], body={'removeLabelIds': ['UNREAD']}).execute()


process_unread_emails()
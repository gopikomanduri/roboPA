import openai
import os
from voice_handler import speak  # assume speak(text) converts to voice output
from voice_handler import listen
import email_handler 


# roboPA openAI key:  "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"
openai.api_key = os.getenv("OPENAI_API_KEY")

def process_query(query):
    context = "...email and slack data here..."
    prompt = f"Context: {context}\n\nUser: {query}\nAssistant:"

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You're an assistant summarizing emails and Slack messages."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]

# def handle_email_command(command: str):
#     if "read" in command and "email" in command:
#         emails = read_unread_emails()
#         if not emails:
#             speak("You have no unread emails.")
#             return
        
#         speak(f"You have {len(emails)} unread emails.")
#         for idx, email in enumerate(emails, 1):
#             speak(f"Email {idx} from {email['sender']}, about {email['subject']}.")
#             speak(f"Summary: {email['snippet']}")

def handle_email_command(command):
    # Fetch unread emails
    emails = email_handler.fetch_unread_emails()

    if not emails:
        speak("You have no unread emails.")
        return

    # Count total emails and responses
    total_emails = len(emails)
    response_emails = len([email for email in emails if "re:" in email.lower() or "fwd:" in email.lower()])

    speak(f"You have {total_emails} unread emails, of which {response_emails} are responses to previous emails.")
    speak("Do you want me to proceed with reading all emails or specific ones?")

    command = listen()

    if "specific" in command:
        speak("Please provide the name or subject you are interested in.")
        name = listen()

        # Filter emails by subject containing the name
        filtered_emails = [email for email in emails if name.lower() in email.lower()]
        filtered_count = len(filtered_emails)
        speak(f"There are {filtered_count} emails related to {name}. Do you want to read them?")

        command = listen()
        if "yes" in command:
            # Read filtered emails (for simplicity, we'll just print them)
            for email in filtered_emails:
                speak(f"Subject: {email}")
                # You can add the logic here to read the email's content
        else:
            speak("Now, I'll check the email body for that name.")
            # Filter by email content (here, you would fetch email bodies and filter them)
            # For simplicity, we’ll assume that the name is in the body
            # Add actual email body content fetch here

            speak(f"There are {filtered_count} emails containing {name} in the subject or body. Do you want to read them?")
            command = listen()
            if "yes" in command:
                for email in filtered_emails:
                    speak(f"Reading email: {email}")
            else:
                speak("No emails to read.")
    else:
        speak("I will proceed with reading all emails.")
        for email in emails:
            speak(f"Subject: {email}")
            # Add email content reading logic here

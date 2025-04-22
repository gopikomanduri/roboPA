from fastapi import FastAPI
from slack_handler import fetch_slack_messages
from agent import process_query
from voice_handler import speak, listen
from agent import handle_email_command

app = FastAPI()

# @app.get("/emails")
# def get_emails():
#     return fetch_emails()

# @app.post("/reply-email")
# def reply_email(email_id: str, content: str):
#     return send_email_reply(email_id, content)

@app.get("/slack-messages")
def get_slack_messages():
    return fetch_slack_messages()

@app.post("/query")
def query_emails_and_slack(query: str):
    return process_query(query)


# def run_voice_agent():
#     while True:
#         speak("How can I help you?")
#         command = listen()
#         print(command)
#         if "email" in command:
#             handle_email_command(command)
#         elif "stop" in command or "exit" in command:
#             speak("Goodbye!")
#             break
#         else:
#             speak("Sorry, I didn’t catch that.")

# run_voice_agent()

def run_voice_agent():
    while True:
        speak("How can I help you?")
        command = listen()
        print(f"Raw Command: {repr(command)}")  # Display the raw string including spaces
        print(f"Length of Command: {len(command)}")  # Check length of the string
        
        if command:  # Check if command is not empty
            print(f"Command received: {command}")
            if "email" in command.strip():  # Remove leading/trailing spaces before checking
                print("yes in email command")
                handle_email_command(command)
            elif "stop" in command or "exit" in command:
                speak("Goodbye!")
                break
            else:
                speak("Sorry, I didn’t catch that.")
        else:
            speak("Sorry, I couldn't hear anything. Please try again.")

run_voice_agent()


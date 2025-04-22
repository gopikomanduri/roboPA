import os
from pathlib import Path

# Define the structure and code content
project_structure = {
    "voice-assistant-mvp": {
        "backend": {
            "main.py": """
from fastapi import FastAPI
from email_handler import fetch_emails, send_email_reply
from slack_handler import fetch_slack_messages
from agent import process_query

app = FastAPI()

@app.get("/emails")
def get_emails():
    return fetch_emails()

@app.post("/reply-email")
def reply_email(email_id: str, content: str):
    return send_email_reply(email_id, content)

@app.get("/slack-messages")
def get_slack_messages():
    return fetch_slack_messages()

@app.post("/query")
def query_emails_and_slack(query: str):
    return process_query(query)
""",

            "email_handler.py": """
def fetch_emails():
    return [{"from": "alice@example.com", "subject": "Project Update", "body": "Here’s what we’ve done..."}]

def send_email_reply(email_id: str, content: str):
    return {"status": "sent", "email_id": email_id, "reply": content}
""",

            "slack_handler.py": """
import os
from slack_sdk import WebClient

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def fetch_slack_messages():
    return [{"from": "bob", "channel": "general", "message": "Hey, can you check the budget?"}]
""",

            "voice_handler.py": """
import speech_recognition as sr
from gtts import gTTS

def speech_to_text(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio = r.record(source)
    return r.recognize_google(audio)

def text_to_speech(text, output_path="output.mp3"):
    tts = gTTS(text)
    tts.save(output_path)
    return output_path
""",

            "agent.py": """
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def process_query(query):
    context = "...email and slack data here..."
    prompt = f"Context: {context}\\n\\nUser: {query}\\nAssistant:"

    response = openai.ChatCompletion.create(
        model="gpt-4-1106-preview",
        messages=[
            {"role": "system", "content": "You're an assistant summarizing emails and Slack messages."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message["content"]
""",

            "config.py": """
# User-specific config to set email filters, slack preferences, etc.
config = {
    "email": {
        "accounts": ["your-email@gmail.com"],
        "filters": {"from": ["boss@example.com"]}
    },
    "slack": {
        "channels": ["general"],
        "dm_only": True
    }
}
"""
        },
        ".env": "OPENAI_API_KEY=\nSLACK_BOT_TOKEN=\n",
        "requirements.txt": """fastapi\nuvicorn\nopenai\ngtts\nspeechrecognition\nslack_sdk\ngoogle-api-python-client\ngoogle-auth\npython-dotenv"""
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = Path(base_path) / name
        if isinstance(content, dict):
            path.mkdir(parents=True, exist_ok=True)
            create_structure(path, content)
        else:
            with open(path, "w", encoding="utf-8") as f:
                f.write(content.strip() + "\n")


if __name__ == "__main__":
    base_path = "."
    create_structure(base_path, project_structure)
    print("✅ Project structure and boilerplate created at ./voice-assistant-mvp")
    print("📦 Next: Run the following commands to get started:")
    print("\ncd voice-assistant-mvp")
    print("python3 -m venv venv && source venv/bin/activate  # (or use venv\\Scripts\\activate on Windows)")
    print("pip install -r requirements.txt")
    print("uvicorn backend.main:app --reload")

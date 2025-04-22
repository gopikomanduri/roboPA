import os
from slack_sdk import WebClient

client = WebClient(token=os.getenv("SLACK_BOT_TOKEN"))

def fetch_slack_messages():
    return [{"from": "bob", "channel": "general", "message": "Hey, can you check the budget?"}]

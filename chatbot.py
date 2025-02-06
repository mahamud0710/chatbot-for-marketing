from flask import Flask, request
import requests
import os

app = Flask(__name__)

# Your Facebook Page Access Token & Verify Token
ACCESS_TOKEN = "EAAIuNEU6hpwBO2Rfdhl0ZAefMOxnZAuZCvKZAUlfFi1gyTduiZCs0N872Cf7UnG5mKOxJIapAYEJlncjwef6fqunJd5y0f2LPkWfXaxeowhwnwQtwhqZAX2TVSdFUh7CGomeQCHz2VqCUJxruT0aZCYhhOMNysZCIdV0gWANE0Xpiw6jYxyhIXbniZCgjDHmyP6qB"
VERIFY_TOKEN = "chatbot_py"

@app.route('/')
def home():
    return "Chatbot is running!"

@app.route('/webhook', methods=['GET'])
def verify():
    """Verify webhook with Facebook"""
    token_sent = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    
    if token_sent == VERIFY_TOKEN:
        return challenge
    return "Verification token mismatch", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming messages from Messenger"""
    data = request.json
    if data.get("object") == "page":
        for entry in data["entry"]:
            for messaging in entry["messaging"]:
                if messaging.get("message"):
                    sender_id = messaging["sender"]["id"]
                    message_text = messaging["message"]["text"]
                    response = process_order(message_text)
                    send_message(sender_id, response)
    return "Message Processed"

def process_order(message_text):
    """Simple order processing logic"""
    message_text = message_text.lower()
    
    if "milk" in message_text or "দুধ" in message_text:
        return "আপনার জন্য কোন ধরনের দুধ লাগবে? (ফুল ফ্যাট / লো ফ্যাট / দেশি গরুর দুধ)"
    
    elif "price" in message_text or "দাম" in message_text:
        return "আমাদের দুধের দাম প্রতি লিটার ৮০ টাকা। আপনি কত লিটার চান?"
    
    elif "order" in message_text or "অর্ডার" in message_text:
        return "অর্ডার দিতে আপনার নাম, ঠিকানা, এবং মোবাইল নাম্বার পাঠান।"
    
    elif "delivery" in message_text or "ডেলিভারি" in message_text:
        return "আমরা ঢাকা ও চট্টগ্রামে ডেলিভারি করি। আপনার লোকেশন জানান।"
    
    elif "hello" in message_text or "হ্যালো" in message_text:
        return "হ্যালো! আমি ন্যুরেশন মিল্কের স্বয়ংক্রিয় চ্যাটবট। আমি আপনাকে কীভাবে সাহায্য করতে পারি?"
    
    else:
        return "দুঃখিত, আমি বুঝতে পারিনি। অনুগ্রহ করে আবার বলুন।"

def send_message(recipient_id, message_text):
    """Send a message to Facebook Messenger"""
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    requests.post(url, headers=headers, json=payload)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)

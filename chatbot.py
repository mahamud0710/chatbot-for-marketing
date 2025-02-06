from flask import Flask, request
import requests

app = Flask(__name__)

# 🔹 Replace this with your actual Facebook Page Access Token
ACCESS_TOKEN = "EAAIuNEU6hpwBO2Rfdhl0ZAefMOxnZAuZCvKZAUlfFi1gyTduiZCs0N872Cf7UnG5mKOxJIapAYEJlncjwef6fqunJd5y0f2LPkWfXaxeowhwnwQtwhqZAX2TVSdFUh7CGomeQCHz2VqCUJxruT0aZCYhhOMNysZCIdV0gWANE0Xpiw6jYxyhIXbniZCgjDHmyP6qB"

@app.route('/')
def home():
    """Default Route - To check if the bot is running"""
    return "✅ Neuration Milk Chatbot is Running!"

@app.route('/webhook', methods=['GET'])
def verify():
    """Facebook Webhook Verification"""
    hub_mode = request.args.get("hub.mode")
    hub_challenge = request.args.get("hub.challenge")
    hub_verify_token = request.args.get("hub.verify_token")

    VERIFY_TOKEN = "YOUR_VERIFY_TOKEN"  # Replace with your own token

    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return hub_challenge
    return "Verification Failed!", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    """Handles incoming messages from Messenger"""
    data = request.json

    if data.get("object") == "page":
        for entry in data.get("entry", []):
            for messaging in entry.get("messaging", []):
                sender_id = messaging.get("sender", {}).get("id")
                message_text = messaging.get("message", {}).get("text", "")

                if sender_id and message_text:
                    response = process_order(message_text)
                    send_message(sender_id, response)

    return "Message Processed", 200

def process_order(message_text):
    """Simple chatbot logic for orders"""
    message_text = message_text.lower()

    if "milk" in message_text or "দুধ" in message_text:
        return "🥛 আপনার জন্য কোন ধরনের দুধ লাগবে? (ফুল ফ্যাট / লো ফ্যাট / দেশি গরুর দুধ)"

    elif "price" in message_text or "দাম" in message_text:
        return "💰 আমাদের দুধের দাম প্রতি লিটার ৮০ টাকা। আপনি কত লিটার চান?"

    elif "order" in message_text or "অর্ডার" in message_text:
        return "📦 অর্ডার দিতে আপনার নাম, ঠিকানা, এবং মোবাইল নাম্বার পাঠান।"

    elif "delivery" in message_text or "ডেলিভারি" in message_text:
        return "🚚 আমরা ঢাকা ও চট্টগ্রামে ডেলিভারি করি। আপনার লোকেশন জানান।"

    elif "hello" in message_text or "হ্যালো" in message_text:
        return "👋 হ্যালো! আমি ন্যুরেশন মিল্কের স্বয়ংক্রিয় চ্যাটবট। কিভাবে সাহায্য করতে পারি?"

    else:
        return "⚠️ দুঃখিত, আমি বুঝতে পারিনি। অনুগ্রহ করে আবার বলুন।"

def send_message(recipient_id, message_text):
    """Send a message to Facebook Messenger"""
    url = f"https://graph.facebook.com/v12.0/me/messages?access_token={ACCESS_TOKEN}"
    headers = {"Content-Type": "application/json"}
    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": message_text}
    }
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"⚠️ Error sending message: {response.text}")

if __name__ == "__main__":
    app.run(port=5000, debug=True)

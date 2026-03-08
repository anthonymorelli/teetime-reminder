from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
BOOKINGS_FILE = "tee_times.csv"
RESPONSES_FILE = "responses.csv"

def get_status(code):
    mapping = {
        "1": "confirmed",
        "2": "cancelled",
        "3": "needs_adjustment"
    }
    return mapping.get(code, "unknown")

def log_response(phone, response_code):
    # Load bookings to find who replied
    bookings = pd.read_csv(BOOKINGS_FILE)
    bookings["phone"] = bookings["phone"].str.strip()

    # Match by phone number
    match = bookings[bookings["phone"] == phone]

    if match.empty:
        print(f"No booking found for {phone}")
        return

    row = match.iloc[0]
    status = get_status(response_code)

    # Build the response record
    response = {
        "booking_id": row["booking_id"],
        "customer_name": row["customer_name"],
        "phone": phone,
        "response_code": response_code,
        "response_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": status
    }

    # Append to responses.csv, create if doesn't exist
    response_df = pd.DataFrame([response])
    file_exists = os.path.exists(RESPONSES_FILE)
    response_df.to_csv(
        RESPONSES_FILE,
        mode="a",
        header=not file_exists,
        index=False
    )
    print(f"✓ Logged: {row['customer_name']} → {status}")

@app.route("/sms", methods=["POST"])
def sms_reply():
    phone = request.form.get("From")
    body = request.form.get("Body", "").strip()
    print(f"Incoming reply from {phone}: {body}")
    log_response(phone, body)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True, port=5000)
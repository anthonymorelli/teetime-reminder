from dotenv import load_dotenv
import os
from twilio.rest import Client
import pandas as pd
from datetime import datetime, timedelta

load_dotenv()
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
api_key = os.getenv("TWILIO_API_KEY_SID")
api_secret = os.getenv("TWILIO_API_KEY_SECRET")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
client = Client(api_key, api_secret, account_sid)

# Load the tee times data 
df = pd.read_csv('tee_times.csv')

# Print the full dataset so we can see what we loaded
print("All bookings:")
print(df)
print()

# Get tommorow's date as a string matching our CSV format
tomorrow = (datetime.today() + timedelta(days=1)).strftime('%Y-%m-%d')
print(f"filtering for: {tomorrow}")
print()

# Filter only tommorow's bookings
tomorrows_bookings = df[df["date"]==tomorrow]

# Print the filtered results 
print("tommorow's bookings:")
print (tomorrows_bookings)

print()
print("Reminder Messages:")
print() 

for index, row in tomorrows_bookings.iterrows():
    message = "Hi " + str(row["customer_name"]) + ", this is Oak Quarry Golf Club. Reminder: you have a tee time tomorrow at " + str(row["tee_time"]) + ". Reply 1 to confirm, 2 to cancel, 3 for changes."
    client.messages.create(
        body=message,
        from_=twilio_number,
        to=str(row["phone"])
    )
    print("Sent to " + str(row["customer_name"]))

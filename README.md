# Tee Time Reminder Automation

Automated SMS reminder system for golf club tee time bookings, built to replace manual customer outreach with a Python-driven pipeline.

## The Problem
Staff at Oak Quarry Golf Club manually called customers before each tee time to confirm bookings — time-consuming and inconsistent. This system automates that process entirely.

## What It Does
- Reads daily booking data from a CSV (sourced from club management software)
- Filters tomorrow's tee times automatically using datetime logic
- Generates personalized SMS reminders for each booking group
- Sends outbound texts via Twilio API
- Captures inbound customer replies (1=confirm, 2=cancel, 3=changes) via Flask webhook
- Logs all responses to a structured CSV for downstream reporting

## Tech Stack
- **Python** — core automation logic
- **pandas** — data ingestion, filtering, and manipulation
- **Twilio REST API** — outbound SMS delivery
- **Flask** — inbound webhook server for capturing customer replies
- **ngrok** — local tunnel for webhook testing
- **python-dotenv** — secure credential management

## Project Structure
teetime-reminder/
├── main.py          # Outbound reminder pipeline
├── webhook.py       # Inbound reply logging via Flask
├── tee_times.csv    # Sample booking data
└── .gitignore       # Excludes .env credentials
## How to Run
1. Clone the repo
2. Install dependencies: `pip install pandas twilio flask python-dotenv`
3. Create a `.env` file with your Twilio credentials:

TWILIO_ACCOUNT_SID=your_sid
TWILIO_API_KEY_SID=your_key
TWILIO_API_KEY_SECRET=your_secret
TWILIO_PHONE_NUMBER=your_number

4. Run outbound reminders: `python3 main.py`
5. Run webhook server: `python3 webhook.py`

## Production Notes
SMS delivery requires A2P 10DLC carrier registration and toll-free number verification for production deployment.
Core automation pipeline is fully functional. 
Integration with live booking data from Quick18/EZSuite tee sheet exports is in progress.

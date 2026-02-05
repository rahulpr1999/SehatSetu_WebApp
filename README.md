# SehatSetu: Rural Healthcare Access Platform

**SehatSetu** is a lightweight, accessible healthcare platform designed for rural India ("Nabha"). It bridges the digital divide by enabling offline-first interactions (IVR/SMS) alongside a modern web interface for doctor booking and medicine inventory management.

## 🚀 Key Features

-   **Patient Registration**: Simple flow with OTP verification and unique 3-digit Patient ID generation.
-   **Smart Booking System**: 
    -   Auto-fills details for registered patients.
    -   Department-based doctor filtering.
    -   Automatic time slot allocation (15-min intervals).
-   **Inventory Management**: Real-time tracking of medicine stock.
-   **IVR Simulator**: Web-based demonstration of voice-based appointment booking (for offline users).
-   **SMS Integration**: Twilio-powered notifications for bookings and reminders.
-   **Optimized UI**: High-contrast, responsive design with auto-fill capabilities.

## 🛠️ Technology Stack

-   **Backend**: Python (Flask), Gunicorn
-   **Database**: AWS DynamoDB (Serverless, Low Cost)
-   **Frontend**: HTML5, TailwindCSS (CDN)
-   **Infrastructure**: AWS EC2 (Ubuntu), Nginx
-   **Services**: Twilio (SMS), AWS Boto3

## 📂 Project Structure

```
├── app.py                 # Main Flask Application
├── templates/             # HTML Templates (Tailwind based)
├── utils/                 # Core Utilities
│   ├── aws_dynamo.py      # DynamoDB Interface
│   ├── otp_service.py     # OTP Logic
│   ├── twilio_client.py   # SMS Wrapper
│   └── config.py          # Configuration
├── requirements.txt       # Python Dependencies
└── COST_ANALYSIS.md       # Financial Cost Breakdown
```

## ⚙️ Setup Instructions

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/rahulpr1999/SehatSetu_WebApp.git
    cd SehatSetu_WebApp
    ```

2.  **Install dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Environment Variables**:
    Create a `.env` file or export variables:
    -   `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
    -   `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`
    -   `TWILIO_PHONE_NUMBER`

4.  **Run Locally**:
    ```bash
    python app.py
    ```

## 💰 Cost Analysis
A detailed financial breakdown is available in [COST_ANALYSIS.md](COST_ANALYSIS.md).
**Estimated Operational Cost**: ~$15/month (Pilot Phase).

## 📄 License
MIT License.

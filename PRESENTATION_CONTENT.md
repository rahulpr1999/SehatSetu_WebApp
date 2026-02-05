# SehatSetu: Hackathon Presentation Content (12 Slides)

**Use this outline to build your pitch deck/PPT. Each section represents a slide.**

---

## Slide 1: Title Slide
**Title:** SehatSetu: Bridging the Healthcare Gap
**Subtitle:** Accessible, Affordable, and Offline-First Healthcare for Rural India
**Team Name:** [Your Team Name]
**Visual:** App Homepage Screenshot / Logo on a clean background

---

## Slide 2: The Problem
**Headline:** The Rural Healthcare Disconnect

-   **Digital Divide:** 50% of rural India lacks reliable internet.
-   **Distance:** Villagers travel 30+ km for basic consultations.
-   **Inventory Blindness:** Patients visit PHCs only to find medicines out of stock.
-   **Inefficiency:** Paper-based records lead to lost history and slow queues.

**Visual:** Image of a crowded rural clinic or someone struggling with signal.

---

## Slide 3: Target Audience (Persona)
**Headline:** Meet Ramesh from Nabha Village

-   **Profile:** 45-year-old farmer, owns a basic feature phone.
-   **Pain Point:** Cannot use complex apps; needs to book a doctor for his child.
-   **Current Reality:** Wastes a day's wage traveling to the city, unsure if the doctor is available.
-   **Need:** A system that works via **Voice (IVR)** or minimal data.

**Visual:** A photo representing a rural user with a feature phone.

---

## Slide 4: Our Solution
**Headline:** Empowering "Nabha" with Hybrid Tech

**SehatSetu** is a dual-mode platform designed for **low-resource environments**.

1.  **Offline-First:** Critical features work via IVR (Voice calling) and SMS.
2.  **Ultra-Light Web:** A fast, high-contrast web app for those with basic smartphones.
3.  **One ID for Life:** Unique 3-digit Patient ID simplifies tracking.

**Visual:** Split screen showing a Phone Call (IVR) vs Web App Dashboard.

---

## Slide 5: Key Features I: Accessibility
**Headline:** No Internet? No Problem.

-   **IVR Simulator:** Patients dialogue with a voice bot to book slots.
-   **SMS Integration:** Instant confirmations and reminders via Twilio.
-   **Language Support:** Designed for vernacular adaptation (Hindi/Regional).
-   **Simple Registration:** OTP-based signup creates a permanent digital identity.

**Visual:** Flowchart of Voice Call -> Appointment Confirmed.

---

## Slide 6: Key Features II: Smart Management
**Headline:** Efficiency for Doctors & Admins

-   **Auto-Fill Booking:** Enter "001" -> System fetches "Rajesh Kumar".
-   **Smart Slotting:** Auto-calculates 15-min intervals to prevent crowding.
-   **Pharmacy Tracker:** Real-time medicine stock view (Red/Green indicators).
-   **Dashboard:** Doctors see today's queue and patient history at a glance.

**Visual:** Screenshot of the Admin Dashboard and Medicine Inventory.

---

## Slide 7: Technology Stack
**Headline:** Built for Scale & Speed

-   **Frontend:** HTML5 + TailwindCSS (High Performance, Responsive)
-   **Backend:** Python Flask (Robust API Logic)
-   **Communication:** Twilio (SMS Automation)
-   **Infra:** AWS EC2 (Reliable Hosting) + Boto3 SDK

**Visual:** Icons of Python, Flask, AWS, Twilio, Tailwind.

---

## Slide 8: System Architecture
**Headline:** Robust & Serverless Design

-   **Database:** AWS DynamoDB
    -   *Why?* Single-digit millisecond latency, scales automatically.
    -   *Cost:* Pay-per-request (Free tier friendly).
-   **Security:**
    -   Role-based access (Patient vs Doctor vs Admin).
    -   Secure OTP verification.

**Visual:** Architecture Diagram (User -> Nginx/Flask -> DynamoDB).

---

## Slide 9: Live Demo / Workflow
**Headline:** The Patient Journey

1.  **Register:** User enters phone -> OTP -> Gets ID `005`.
2.  **Book:** User opens Booking Page -> Enters `005` -> Name auto-appears.
3.  **Confirm:** SMS received with Token Number.
4.  **Visit:** Doctor manages queue on dashboard.

**Visual:** A step-by-step screenshot strip of the actual app flow.

---

## Slide 10: Financial Viability
**Headline:** Sustainable & Cost-Effective

**Monthly Operating Cost (Pilot): ~$15 USD**

| Component | Cost | Why? |
| :--- | :--- | :--- |
| **AWS Infrastructure** | **~$0** | Free Tier (EC2 + DynamoDB) |
| **SMS (Twilio)** | **~$15** | Variable (1000 SMS est.) |
| **Maintenance** | **Minimal** | Serverless DB = Zero Admin |

**Visual:** A simple pie chart showing costs (mostly SMS).

---

## Slide 11: Future Roadmap
**Headline:** What's Next for SehatSetu?

-   **Phase 2:** AI Symptom Checker (Chatbot integration).
-   **Phase 3:** IoT Integration for remote vitals monitoring (BP/Heart Rate).
-   **Phase 4:** Video Consultations (WebRTC) for remote diagnosis.

**Visual:** A timeline graphic (Now -> Next 6 Months -> Year 1).

---

## Slide 12: Why We Win (Conclusion)
**Headline:** Health for All, No Matter Where.

-   **Impact:** Reduces travel time by 90%.
-   **Scalability:** Can serve 100 or 100,000 villages.
-   **Readiness:** Deployed and functional **today**.

**Thank You!**
[GitHub Repo Link] | [Live Demo Link]

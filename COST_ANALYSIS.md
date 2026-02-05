# Financial Cost Analysis: Nabha Rural Healthcare Platform

## Executive Summary
This document outlines the estimated monthly operational costs for running the SehatSetu platform. The architecture benefits significantly from AWS Free Tier eligibility for the first 12 months, keeping initial fixed costs near zero. The primary variable cost will be SMS notifications (Twilio).

| Item | Monthly Cost (Approx) | Notes |
| :--- | :--- | :--- |
| **Infrastructure (AWS)** | **$0 - $12** | Free Tier eligible (Year 1) |
| **SMS Services (Twilio)** | **Variable** | ~$0.014 per SMS |
| **Domain & DNS** | **$1 - $2** | Route 53 (Optional) |
| **TOTAL ESTIMATE** | **~$15 / month** | Assuming 1,000 SMS/month |

---

## 1. Infrastructure Infrastructure (AWS)

### Compute (EC2)
Hosting the Flask Application via Gunicorn/Nginx.
- **Instance Type**: `t3.micro` (2 vCPU, 1GB RAM) - Sufficient for ~50 concurrent users.
- **Region**: Asia Pacific (Mumbai) `ap-south-1`
- **Cost**:
    - **Year 1 (Free Tier)**: **$0.00** (750 hours/month free for t2.micro/t3.micro)
    - **Standard Price**: **~$10.44 / month** (On-Demand)
- **Recommendation**: Reserve instance for 1 year to reduce cost to **~$6.50/month**.

### Database (DynamoDB)
Storing Patient, Doctor, and Appointment records.
- **Capacity Mode**: On-Demand (Pay-per-request).
- **Cost**:
    - **Storage**: 25 GB free forever.
    - **Reads/Writes**: 200 Million requests free monthly.
- **Estimated Cost**: **$0.00** (Highly unlikely to exceed Free Tier limits for this scale).

### Network & Security
- **Data Transfer**: First 100GB/month out to internet is free.
- **Elastic IP**: Free while attached to running instance.

---

## 2. Operational Costs (Variable)

### SMS Notifications (Twilio)
Used for OTPs, Booking Confirmations, and Reminders. This is the main scaling cost.
- **Pricing (India)**: ~$0.0140 per SMS segment (varies by carrier).
- **Phone Number Rental**: ~$1.15 / month.

**Scenario A: Low Volume (Pilot)**
- 500 SMS/month (approx. 150 bookings)
- Cost: (500 * $0.014) + $1.15 = **~$8.15 / month**

**Scenario B: Medium Volume**
- 2,000 SMS/month (approx. 600 bookings)
- Cost: (2000 * $0.014) + $1.15 = **~$29.15 / month**

### Domain Name (Route 53)
- **Domain Registration**: ~$12 - $15 / year (e.g., .com, .in).
- **DNS Zone**: $0.50 / month.

---

## 3. Potential Future Costs

If the platform scales significantly, consider these upgrades:

| Service | Upgrade Trigger | Estimated Cost |
| :--- | :--- | :--- |
| **Amazon Connect** | Real IVR Implementation | ~$0.018/min inbound |
| **AWS S3** | Storing prescription images | ~$0.023/GB |
| **Load Balancer** | High availability (>500 users) | ~$16/month |

## Conclusion
For the initial launch and hackathon phase, the platform cost is effectively **driven only by SMS usage**. The infrastructure is robust and free-tier compliant.

**Recommendation**: Cap SMS usage or switch to AWS SNS (Sender ID required for India) for lower bulk rates in production ($0.002 - $0.004 per SMS depending on DLT registration).

from flask import Blueprint, request, url_for
from twilio.twiml.voice_response import VoiceResponse
from utils.aws_dynamo import DynamoDBClient

ivr = Blueprint('ivr', __name__)
db_client = DynamoDBClient()

@ivr.route("/voice", methods=['GET', 'POST'])
def welcome():
    """Returns TwiML for the initial IVR Menu."""
    resp = VoiceResponse()
    with resp.gather(num_digits=1, action=url_for('ivr.menu'), method='POST') as g:
        g.say("Namaste! Welcome to Sehat Setu. Press 1 for Doctor Appointment. Press 2 for New Registration.", loop=3, language='en-IN')
    return str(resp)

@ivr.route("/voice/menu", methods=['POST'])
def menu():
    selected_option = request.form['Digits']
    option_actions = {
        '1': appointment_flow,
        '2': registration_flow,
    }

    if selected_option in option_actions:
        response = option_actions[selected_option]()
        return str(response)
    
    resp = VoiceResponse()
    resp.say("Invalid choice. Please try again.")
    resp.redirect(url_for('ivr.welcome'))
    return str(resp)

def appointment_flow():
    resp = VoiceResponse()
    resp.say("You selected Doctor Appointment.", language='en-IN')
    with resp.gather(num_digits=4, action=url_for('ivr.check_reg'), method='POST') as g:
        g.say("Please enter the last 4 digits of your Registration Number or Phone Number.", language='en-IN')
    return resp

def registration_flow():
    resp = VoiceResponse()
    resp.say("To register, please visit our website or visit the hospital reception. Dhanyavad.", language='en-IN')
    resp.hangup()
    return resp

@ivr.route("/voice/check_reg", methods=['POST'])
def check_reg():
    digits = request.form['Digits']
    resp = VoiceResponse()
    
    # Mock lookup or DB lookup logic
    # In a real app, we'd query DynamoDB for a user with this ID/Phone
    # For Hackathon, let's pretend we found them and offer a slot
    
    resp.say(f"We found your record for ID ending in {digits}.", language='en-IN')
    
    # Check availability (Example: Fetch next available slot for Dr. Sharma)
    # Using our DB client
    # simple MVP logic:
    
    try:
        # Just offer the first available doctor from our DB
        doctors = db_client.get_all_doctors()
        if doctors:
            doc = doctors[0]
            resp.say(f"The next available slot for {doc['name']} is tomorrow at 10 AM. Press 1 to confirm booking.", language='en-IN')
            resp.gather(num_digits=1, action=url_for('ivr.confirm_booking', doctor_id=doc['id']), method='POST')
        else:
            resp.say("Sorry, no doctors are currently available.", language='en-IN')
    except Exception as e:
         resp.say("We are facing technical difficulties.", language='en-IN')
         
    return str(resp)

@ivr.route("/voice/confirm_booking", methods=['POST'])
def confirm_booking():
    digit = request.form['Digits']
    doctor_id = request.args.get('doctor_id')
    
    resp = VoiceResponse()
    if digit == '1':
        # Create appointment in DB (MVP: Minimal data)
        # In prod, we'd need patient ID from previous step
        import uuid
        import datetime
        from datetime import timezone, timedelta
        IST = timezone(timedelta(hours=5, minutes=30))
        
        appt_id = str(uuid.uuid4())
        # We don't have patient name from voice, so using 'Voice Caller'
        item = {
            'id': appt_id,
            'doctor_id': doctor_id,
            'patient_name': 'Voice Caller', 
            'phone': request.form.get('From', 'Unknown'),
            'type': 'physical',
            'date': (datetime.datetime.now(IST) + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '10:00',
            'status': 'confirmed',
            'created_at': datetime.datetime.now(IST).isoformat()
        }
        db_client.add_appointment(item)
        
        resp.say("Your appointment has been confirmed. You will receive an SMS shortly. Dhanyavad.", language='en-IN')
    else:
        resp.say("Booking cancelled. Dhanyavad.", language='en-IN')
        
    return str(resp)

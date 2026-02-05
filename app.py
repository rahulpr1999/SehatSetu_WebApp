from flask import Flask, render_template, request, redirect, url_for, flash, session
import uuid
import datetime
import pytz

# Define IST Timezone using pytz
IST = pytz.timezone('Asia/Kolkata')
from utils.aws_dynamo import DynamoDBClient
from utils.twilio_client import TwilioClient
from utils.otp_service import OTPService

from config import Config

app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize Clients
db_client = DynamoDBClient()
sms_client = TwilioClient()
otp_service = OTPService()


import traceback
from ivr_routes import ivr
app.register_blueprint(ivr)

# --- IVR SIMULATOR ROUTES ---
@app.route('/ivr-demo')
def ivr_demo():
    return render_template('ivr_simulator.html')

@app.route('/api/ivr/get-doctor', methods=['GET'])
def api_get_doctor():
    # Helper for Simulator to get a doctor
    try:
        doctors = db_client.get_all_doctors()
        if doctors:
            doc = doctors[0]
            return {"status": "success", "doctor_name": doc['name'], "doctor_id": doc['id'], "slot_time": "10:00 AM"}
        return {"status": "failed"}
    except:
        return {"status": "error"}

@app.route('/api/ivr/book', methods=['POST'])
def api_book_appt():
    try:
        data = request.json
        doctor_id = data.get('doctor_id')
        
        # IST Time
        IST = timezone(timedelta(hours=5, minutes=30))
        appt_id = str(uuid.uuid4())
        
        item = {
            'id': appt_id,
            'doctor_id': doctor_id,
            'patient_name': 'Demo Caller', 
            'phone': '9999999999', 
            'type': 'physical',
            'date': (datetime.datetime.now(IST) + datetime.timedelta(days=1)).strftime('%Y-%m-%d'),
            'time': '10:00',
            'status': 'confirmed',
            'created_at': datetime.datetime.now(IST).isoformat()
        }
        db_client.add_appointment(item)
        return {"status": "success", "id": appt_id}
    except Exception as e:
        print(e)
        return {"status": "error"}


@app.errorhandler(500)
def internal_error(exception):
    print("CRITICAL 500 ERROR:")
    print(traceback.format_exc())
    return "Internal Server Error: " + str(exception), 500

@app.errorhandler(Exception)
def handle_exception(e):
    print("UNHANDLED EXCEPTION:")
    print(traceback.format_exc())
    return "Internal Server Error: " + str(e), 500


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/medicines')
def medicines():
    medicines = db_client.get_all_medicines()
    print(f"DEBUG: Found {len(medicines)} medicines")
    return render_template('medicines.html', medicines=medicines)

# ===== PATIENT REGISTRATION ROUTES =====

@app.route('/register')
def register():
    """Patient registration page."""
    return render_template('register.html')

@app.route('/api/send-otp', methods=['POST'])
def send_otp():
    """Generate and send OTP to phone number."""
    try:
        data = request.get_json()
        phone = data.get('phone')
        
        if not phone:
            return {'success': False, 'message': 'Phone number is required'}, 400
        
        # Check if patient already registered
        existing_patient = db_client.get_patient_by_phone(phone)
        if existing_patient:
            return {
                'success': False, 
                'message': f'Phone number already registered with Patient ID: {existing_patient["patient_id"]}',
                'patient_id': existing_patient['patient_id']
            }, 400
        
        # Generate OTP
        otp = otp_service.generate_otp(phone)
        
        # Send OTP via SMS
        message = f"Your OTP for Nabha Healthcare registration is: {otp}. Valid for 10 minutes."
        sms_sent = sms_client.send_sms(phone, message)
        
        if sms_sent:
            return {'success': True, 'message': 'OTP sent successfully'}, 200
        else:
            return {'success': False, 'message': 'Failed to send OTP. Please try again.'}, 500
            
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return {'success': False, 'message': str(e)}, 500

@app.route('/api/verify-otp', methods=['POST'])
def verify_otp():
    """Verify OTP for phone number."""
    try:
        data = request.get_json()
        phone = data.get('phone')
        otp = data.get('otp')
        
        if not phone or not otp:
            return {'success': False, 'message': 'Phone and OTP are required'}, 400
        
        # Verify OTP
        is_valid = otp_service.verify_otp(phone, otp)
        
        if is_valid:
            return {'success': True, 'message': 'OTP verified successfully'}, 200
        else:
            return {'success': False, 'message': 'Invalid or expired OTP'}, 400
            
    except Exception as e:
        print(f"Error verifying OTP: {e}")
        return {'success': False, 'message': str(e)}, 500

@app.route('/api/complete-registration', methods=['POST'])
def complete_registration():
    """Complete patient registration after OTP verification."""
    try:
        data = request.get_json()
        phone = data.get('phone')
        name = data.get('name')
        age = data.get('age')
        
        if not all([phone, name, age]):
            return {'success': False, 'message': 'All fields are required'}, 400
        
        # Create patient record
        patient = db_client.create_patient(phone, name, age)
        
        if patient:
            return {
                'success': True,
                'message': 'Registration successful!',
                'patient': {
                    'patient_id': patient['patient_id'],
                    'name': patient['name'],
                    'phone': patient['phone'],
                    'age': patient['age']
                }
            }, 200
        else:
            return {'success': False, 'message': 'Registration failed'}, 500
            
    except Exception as e:
        print(f"Error completing registration: {e}")
        return {'success': False, 'message': str(e)}, 500

@app.route('/api/get-patient/<patient_id>', methods=['GET'])
def get_patient(patient_id):
    """Get patient details by patient ID for auto-fill."""
    try:
        patient = db_client.get_patient_by_id(patient_id)
        
        if patient:
            return {
                'success': True,
                'patient': {
                    'patient_id': patient['patient_id'],
                    'name': patient['name'],
                    'phone': patient['phone'],
                    'age': patient.get('age', '')
                }
            }, 200
        else:
            return {'success': False, 'message': 'Patient not found'}, 404
            
    except Exception as e:
        print(f"Error fetching patient: {e}")
        return {'success': False, 'message': str(e)}, 500

@app.route('/book', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        # Extract form data
        doctor_id = request.form.get('doctor_id')
        patient_name = request.form.get('patient_name')
        phone = request.form.get('phone')
        appt_type = request.form.get('appointment_type')
        date = request.form.get('date')
        time_slot = request.form.get('time')
        
        # Simple Validation
        if not all([doctor_id, patient_name, phone, date, time_slot]):
            return "Missing mandatory fields", 400

        # Validate: Prevent booking past dates/times
        try:
            booking_datetime = datetime.datetime.strptime(f"{date} {time_slot}", "%Y-%m-%d %H:%M")
            booking_datetime_ist = IST.localize(booking_datetime)
            current_time_ist = datetime.datetime.now(IST)
            
            if booking_datetime_ist < current_time_ist:
                flash("Cannot book appointments in the past. Please select a future date and time.", "error")
                return "Cannot book appointments in the past. Please select a future date and time.", 400
        except ValueError:
            return "Invalid date or time format", 400

        # Validate working hours (9 AM - 12 PM, 1:30 PM - 4:30 PM)
        time_parts = time_slot.split(':')
        hour = int(time_parts[0])
        minute = int(time_parts[1])
        
        # Convert to minutes for easier comparison
        time_in_minutes = hour * 60 + minute
        morning_start = 9 * 60  # 9:00 AM
        morning_end = 12 * 60   # 12:00 PM
        afternoon_start = 13 * 60 + 30  # 1:30 PM
        afternoon_end = 16 * 60 + 30    # 4:30 PM
        
        # Check if time falls within working hours
        is_morning_slot = morning_start <= time_in_minutes < morning_end
        is_afternoon_slot = afternoon_start <= time_in_minutes < afternoon_end
        
        if not (is_morning_slot or is_afternoon_slot):
            return "Appointments are only available from 9:00 AM to 12:00 PM and 1:30 PM to 4:30 PM.", 400

        # Check for conflicts
        if db_client.check_appointment_conflict(doctor_id, date, time_slot):
             flash("This time slot is already booked. Please choose another.", "error")
             return "This time slot is already booked.", 400
             
        # Advanced Availability Check
        doctor = db_client.get_doctor_by_id(doctor_id)
        if doctor and 'schedule' in doctor and doctor['schedule']:
            day_schedule = doctor['schedule'].get(date)
            # If a specific schedule exists for this day
            if day_schedule:
                if not day_schedule.get('available', True):
                     return "Doctor is not available on this day.", 400
                
                # Check time range
                start_time = day_schedule.get('start', '09:00')
                end_time = day_schedule.get('end', '17:00')
                
                if time_slot < start_time or time_slot > end_time:
                    return f"Doctor is only available between {start_time} and {end_time}.", 400

        # Generate Appointment ID, Token Number, and fetch doctor details
        appt_id = str(uuid.uuid4())
        
        # Generate Token Number (format: YYYYMMDD-XXX where XXX is sequential)
        today_str = datetime.datetime.now(IST).strftime("%Y%m%d")
        # Count today's appointments to generate next token
        all_appointments = db_client.get_all_appointments()
        today_count = len([a for a in all_appointments if a.get('created_at', '').startswith(today_str)])
        token_number = f"{today_str}-{(today_count + 1):03d}"
        
        # Fetch doctor details
        doctor = db_client.get_doctor_by_id(doctor_id)
        doctor_name = doctor.get('name', 'Unknown') if doctor else 'Unknown'
        
        video_link = None
        if appt_type == 'virtual':
            video_link = None

        appointment_item = {
            'id': appt_id,
            'token_number': token_number,
            'doctor_id': doctor_id,
            'doctor_name': doctor_name,
            'patient_name': patient_name,
            'phone': phone,
            'type': appt_type,
            'date': date,
            'time': time_slot,
            'video_link': video_link,
            'status': 'confirmed',
            'created_at': datetime.datetime.now(IST).isoformat()
        }

        # Save to DynamoDB
        success = db_client.add_appointment(appointment_item)
        
        if success:
            # Send SMS
            # Force URL to be the EC2 public DNS if running on localhost but sending to world
            # (Hack for demo: if local, replace with hardcoded EC2 URL so phone can open it)
            final_link = video_link
            if video_link and ('127.0.0.1' in video_link or 'localhost' in video_link):
                 final_link = f"http://ec2-40-192-26-159.ap-south-2.compute.amazonaws.com:5000/patient/waiting_room/{appt_id}"

            # Enhanced SMS with token number and doctor name
            msg = f"Hello {patient_name}, your appointment is confirmed!\nToken: {token_number}\nDoctor: {doctor_name}\nDate: {date}\nTime: {time_slot}\nVenue: Civil Hospital"
            if video_link:
                msg += f"\nJoin: {final_link}"
            
            sms_client.send_sms(phone, msg)
            
            # Restore doctor object fetch and correct template name
            doctor = db_client.get_doctor_by_id(doctor_id) # Re-fetch doctor object if needed for success page
            return render_template('success.html', appointment=appointment_item, doctor=doctor)
        else:
            return "Failed to book appointment. Please try again.", 500

    # GET request: fetch doctors to populate the dropdown
    doctors = db_client.get_all_doctors()
    return render_template('book.html', doctors=doctors)

app.secret_key = 'super-secret-key-for-hackathon' # In prod, use config

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if already logged in
    if 'user_role' in session:
        if session['user_role'] == 'admin':
            return redirect(url_for('admin_dashboard'))
        elif session['user_role'] == 'doctor':
             return redirect(url_for('doctor_dashboard', doctor_id=session.get('doctor_id')))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple hardcoded auth for Hackathon MVP
        if username == 'admin' and password == 'admin123':
            session['user_role'] = 'admin'
            return redirect(url_for('admin_dashboard'))
        elif username.startswith('doc_'):
            # Assume doctor login: doc_ID
            doc_id = username.split('_')[1]
            session['user_role'] = 'doctor'
            session['doctor_id'] = doc_id
            return redirect(url_for('doctor_dashboard', doctor_id=doc_id))
        else:
            return "Invalid Credentials", 401
            
    return render_template('login.html')


# --- Admin Routes ---
@app.route('/admin/dashboard')
def admin_dashboard():
    if session.get('user_role') != 'admin':
        return redirect(url_for('login'))

    doctors = db_client.get_all_doctors()
    medicines = db_client.get_all_medicines()
    appointments = db_client.get_all_appointments()
    
    # Filter for video sessions (or show all)
    # We pass all to template, template handles display
    response = render_template('dashboard_admin.html', doctors=doctors, medicines=medicines, appointments=appointments)
    
    # Prevent Caching
    response = app.make_response(response)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/admin/add_doctor', methods=['POST'])
def add_doctor():
    name = request.form.get('name')
    dept = request.form.get('department')
    doc_id = str(uuid.uuid4())
    
    db_client.add_doctor({
        'id': doc_id,
        'name': name,
        'department': dept,
        'available_slots': ['09:00', '10:00', '11:00', '14:00'] # Default slots
    })
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete_doctor', methods=['POST'])
def delete_doctor():
    doc_id = request.form.get('doctor_id')
    db_client.delete_doctor(doc_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/edit_doctor/<doctor_id>', methods=['GET'])
def edit_doctor(doctor_id):
    doctor = db_client.get_doctor_by_id(doctor_id)
    if not doctor:
        return "Doctor not found", 404
    return render_template('edit_doctor.html', doctor=doctor)

@app.route('/admin/update_doctor', methods=['POST'])
def update_doctor():
    doc_id = request.form.get('doctor_id')
    name = request.form.get('name')
    dept = request.form.get('department')
    
    db_client.update_doctor(doc_id, name, dept)
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/add_medicine', methods=['POST'])
def add_medicine():
    print("DEBUG: Entered add_medicine")
    try:
        name = request.form.get('name')
        print(f"DEBUG: Name={name}")
        # Default to False if unchecked, True if checked (which sends 'on')
        # But template has checked by default, so it sends 'on'
        is_in_stock = request.form.get('in_stock') == 'on' 
        print(f"DEBUG: Stock={is_in_stock}")
        med_id = str(uuid.uuid4())
        print(f"DEBUG: ID={med_id}")
        
        success = db_client.add_medicine({
            'id': med_id,
            'name': name,
            'in_stock': is_in_stock
        })
        print(f"DEBUG: DB Add Result={success}")
        if not success:
            raise Exception("DB failed to add medicine")
            
        return redirect(url_for('admin_dashboard'))
    except Exception as e:
        print(f"ERROR in add_medicine: {e}")
        print(traceback.format_exc())
        raise e



@app.route('/admin/delete_medicine', methods=['POST'])
def delete_medicine():
    med_id = request.form.get('medicine_id')
    db_client.delete_medicine(med_id)
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/toggle_stock', methods=['POST'])
def toggle_stock():
    med_id = request.form.get('medicine_id')
    current_status = request.form.get('current_status') == 'True'
    db_client.update_medicine_stock(med_id, not current_status)
    return redirect(url_for('admin_dashboard'))

# --- Doctor Routes ---
@app.route('/doctor/dashboard/<doctor_id>')
def doctor_dashboard(doctor_id):
    if session.get('user_role') != 'doctor' and session.get('user_role') != 'admin':
         return redirect(url_for('login'))

    # Strict check if logged in doctor matches requested doctor_id (unless admin)
    if session.get('user_role') == 'doctor' and session.get('doctor_id') != doctor_id:
        return "Unauthorized access to this doctor's dashboard", 403

    doctor = db_client.get_doctor_by_id(doctor_id)
    if not doctor:
        return "Doctor not found", 404
        
    appointments = db_client.get_appointments_by_doctor(doctor_id)
    
    # Generate next 5 days for the schedule interface
    today = datetime.date.today()
    next_5_days = []
    
    for i in range(5):
        day = today + datetime.timedelta(days=i)
        date_str = day.isoformat()
        
        # Get existing settings if any
        existing = {}
        if 'schedule' in doctor and doctor['schedule'] and date_str in doctor['schedule']:
            existing = doctor['schedule'][date_str]
            
        next_5_days.append({
            'date': date_str,
            'day_name': day.strftime('%A'),
            'available': existing.get('available', True), # Default to True
            'start': existing.get('start', '09:00'),
            'end': existing.get('end', '17:00')
        })
        
    response = render_template('dashboard_doctor.html', doctor=doctor, appointments=appointments, schedule_days=next_5_days)
    
    # Prevent Caching
    response = app.make_response(response)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

# --- Doctor Actions ---
@app.route('/doctor/appointment/update_status', methods=['POST'])
def update_appointment_status():
    if session.get('user_role') != 'doctor' and session.get('user_role') != 'admin':
        return "Unauthorized", 403
        
    appt_id = request.form.get('appointment_id')
    status = request.form.get('status') # 'confirmed' or 'rejected'
    
    db_client.update_appointment_status(appt_id, status)
    
    # Notify Patient
    appt = db_client.get_appointment(appt_id)
    if appt:
        msg = f"Your appointment status has been updated to: {status.upper()}."
        if status == 'rejected':
            msg += " Please contact the clinic for rescheduling."
        sms_client.send_sms(appt['phone'], msg)
        
    return redirect(request.referrer)

@app.route('/doctor/appointment/reschedule', methods=['POST'])
def reschedule_appointment():
    if session.get('user_role') != 'doctor' and session.get('user_role') != 'admin':
        return "Unauthorized", 403
        
    appt_id = request.form.get('appointment_id')
    new_date = request.form.get('new_date')
    new_time = request.form.get('new_time')
    
    db_client.reschedule_appointment(appt_id, new_date, new_time)
    
    # Notify Patient
    appt = db_client.get_appointment(appt_id)
    if appt:
        msg = f"Your appointment has been RESCHEDULED to {new_date} at {new_time} by Dr. {session.get('doctor_id')}."
        sms_client.send_sms(appt['phone'], msg)
        
    return redirect(request.referrer)

@app.route('/doctor/schedule/update', methods=['POST'])
def update_doctor_schedule():
    print("DEBUG: Entered update_doctor_schedule")
    try:
        if session.get('user_role') != 'doctor' and session.get('user_role') != 'admin':
            return "Unauthorized", 403
            
        doctor_id = session.get('doctor_id') or request.form.get('doctor_id')
        print(f"DEBUG: Doctor ID={doctor_id}")
        
        # Parse form data for 5 days
        # Expected format: date_0, available_0, start_0, end_0 ...
        schedule_data = {}
        
        # We iterate through the form based on known keys or structure
        # A cleaner way is to reconstruct it based on the dates passed hidden
        
        # Let's assume we pass a list of dates in the form
        dates = request.form.getlist('dates[]')
        print(f"DEBUG: Dates={dates}")
        
        for date in dates:
            available = request.form.get(f'available_{date}') == 'on'
            start = request.form.get(f'start_{date}')
            end = request.form.get(f'end_{date}')
            
            schedule_data[date] = {
                'available': available,
                'start': start,
                'end': end
            }
            
        print(f"DEBUG: Schedule Data={schedule_data}")
        db_client.update_doctor_schedule(doctor_id, schedule_data)
        flash("Schedule updated successfully!", "success")
        return redirect(url_for('doctor_dashboard', doctor_id=doctor_id))
    except Exception as e:
        print(f"ERROR in update_doctor_schedule: {e}")
        print(traceback.format_exc())
        raise e

# --- Logout Route ---
@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Binds to all interfaces (0.0.0.0) to make it accessible externally on EC2
    app.run(host='0.0.0.0', port=5000, debug=False)


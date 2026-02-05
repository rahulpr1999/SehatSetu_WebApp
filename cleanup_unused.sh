#!/bin/bash
# Cleanup script to remove unused files

echo "🧹 Cleaning up unused files..."

# Remove video conference files
rm -f templates/video_call.html
rm -f templates/waiting_room.html
rm -f templates/meeting_ended.html
rm -f utils/aws_chime.py
echo "✓ Removed video conference files"

# Remove AWS Connect setup files
rm -f aws_connect_lambda.py
rm -f setup_connect_full.py
rm -f deploy_lambda_backend.py
rm -f check_connect_perms.py
echo "✓ Removed AWS Connect setup files"

# Remove diagnostic and test files
rm -f diagnose.py
rm -f check_creds.py
rm -f debug_import.py
rm -f test_boto.py
rm -f test_video_flow.py
rm -f verify_keys.py
rm -f verify_old_keys.py
rm -f check_appointments.py
rm -f check_db_integrity.py
rm -f check_hardcoded.py
rm -f send_test_sms.py
echo "✓ Removed diagnostic/test files"

# Remove cleanup scripts
rm -f cleanup_db_video.py
rm -f clear_db.py
echo "✓ Removed cleanup scripts"

# Remove setup scripts
rm -f setup_resources.py
rm -f start.sh
echo "✓ Removed old setup scripts"

# Remove unused utilities
rm -f utils/aws_sns.py
echo "✓ Removed unused utilities"

# Clean up Python cache
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
find . -type f -name "*.pyc" -delete 2>/dev/null
echo "✓ Cleaned Python cache"

echo ""
echo "✅ Cleanup complete!"
echo ""
echo "Remaining essential files:"
echo "  - app.py (main application)"
echo "  - ivr_routes.py (IVR routes)"
echo "  - seed_doctors.py, seed_medicines.py (data seeding)"
echo "  - create_patients_table.py (table creation)"
echo "  - start_server.sh (server startup)"
echo "  - requirements.txt (dependencies)"
echo "  - utils/: aws_dynamo.py, config.py, otp_service.py, twilio_client.py"
echo "  - templates/: 10 active templates"

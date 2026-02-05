#!/bin/bash
# Server cleanup script

# 1. Remove unused diagnostic/test files
rm -f /home/ubuntu/app_new/diagnose.py
rm -f /home/ubuntu/app_new/check_creds.py
rm -f /home/ubuntu/app_new/debug_import.py
rm -f /home/ubuntu/app_new/test_boto.py
rm -f /home/ubuntu/app_new/test_video_flow.py
rm -f /home/ubuntu/app_new/verify_keys.py
rm -f /home/ubuntu/app_new/verify_old_keys.py
rm -f /home/ubuntu/app_new/check_appointments.py
rm -f /home/ubuntu/app_new/check_db_integrity.py
rm -f /home/ubuntu/app_new/check_hardcoded.py
rm -f /home/ubuntu/app_new/send_test_sms.py
rm -f /home/ubuntu/app_new/cleanup_db_video.py
rm -f /home/ubuntu/app_new/clear_db.py

# 2. Remove AWS Connect setup files
rm -f /home/ubuntu/app_new/aws_connect_lambda.py
rm -f /home/ubuntu/app_new/setup_connect_full.py
rm -f /home/ubuntu/app_new/deploy_lambda_backend.py
rm -f /home/ubuntu/app_new/check_connect_perms.py

# 3. Remove old/misplaced HTML and Utils
rm -f /home/ubuntu/app_new/video_call.html
rm -f /home/ubuntu/app_new/waiting_room.html
rm -f /home/ubuntu/app_new/meeting_ended.html
rm -f /home/ubuntu/app_new/register.html  # Should be in templates/
rm -f /home/ubuntu/app_new/success.html   # Should be in templates/
rm -f /home/ubuntu/app_new/aws_dynamo.py  # Should be in utils/
rm -f /home/ubuntu/app_new/config.py      # Should be in utils/
rm -f /home/ubuntu/app_new/otp_service.py # Should be in utils/
rm -f /home/ubuntu/app_new/app.py.bak*

# 4. Remove unused Utils inside utils folder
rm -f /home/ubuntu/app_new/utils/aws_sns.py
rm -f /home/ubuntu/app_new/utils/aws_chime.py

# 5. Remove old scripts
rm -f /home/ubuntu/app_new/setup_resources.py
rm -f /home/ubuntu/app_new/start.sh

# 6. Clean pycache
find /home/ubuntu/app_new -name "__pycache__" -type d -exec rm -rf {} +

echo "Server cleanup complete."

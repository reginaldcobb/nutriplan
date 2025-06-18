#!/bin/bash
cd /opt/nutriplan/backend
source venv/bin/activate
nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
echo "✅ Django server started on port 8000"

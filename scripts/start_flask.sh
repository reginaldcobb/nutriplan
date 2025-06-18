#!/bin/bash
cd /opt/nutriplan/api_proxy
source venv/bin/activate
nohup python src/main.py > flask.log 2>&1 &
echo "✅ Flask API proxy started on port 5001"

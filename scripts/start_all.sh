#!/bin/bash
echo "🚀 Starting all services..."

# Start Django
echo "🔹 Starting Django server..."
/opt/nutriplan/scripts/start_django.sh

# Start Flask API Proxy
echo "🔹 Starting Flask API proxy..."
/opt/nutriplan/scripts/start_flask.sh

# Start React Dev Server
echo "🔹 Starting React frontend..."
/opt/nutriplan/scripts/start_react.sh

echo "✅ All services started successfully!"

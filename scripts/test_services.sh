#!/bin/bash
echo "🔍 Testing Django API..."
curl "http://localhost:8000/api/foods/stats/"

echo "🔍 Testing Flask API proxy..."
curl "http://localhost:5001/api/status"

echo "🔍 Testing food search endpoint..."
curl "http://localhost:8000/api/foods/search/?q=chicken"

echo "🔍 Testing React frontend..."
curl "http://localhost:5173"

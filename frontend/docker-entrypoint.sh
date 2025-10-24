#!/bin/sh
# ============================================
# Docker Entrypoint Script
# Injects runtime environment variables into config.js
# ============================================

set -e

echo "🚀 Starting frontend container..."
echo "📡 API_BASE_URL: ${API_BASE_URL}"

# Replace placeholders in config.js.template
envsubst '${API_BASE_URL}' < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js

# Replace placeholders in nginx.conf.template
envsubst '${API_BASE_URL}' < /etc/nginx/conf.d/default.conf.template > /etc/nginx/conf.d/default.conf

echo "✅ Configuration files generated"
echo "🌐 Starting Nginx..."

# Start Nginx
exec nginx -g 'daemon off;'

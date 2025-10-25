# ============================================
# Frontend Dockerfile (React + Vite + Nginx for Render)
# ============================================

# ---- Build Stage ----
FROM node:20-alpine AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# ---- Production Stage ----
FROM nginx:alpine

# Render will inject $PORT and $API_BASE_URL automatically
ENV PORT=8080
ENV API_BASE_URL=https://example.com

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx and config templates
COPY frontend/nginx.conf.template /etc/nginx/templates/default.conf.template
COPY frontend/public/config.js.template /usr/share/nginx/html/config.js.template

# Generate dynamic config on container start
CMD ["/bin/sh", "-c", \
  "envsubst '$$PORT' < /etc/nginx/templates/default.conf.template > /etc/nginx/conf.d/default.conf && \
   envsubst '$$API_BASE_URL' < /usr/share/nginx/html/config.js.template > /usr/share/nginx/html/config.js && \
   exec nginx -g 'daemon off;'"]

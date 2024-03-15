# Build the frontend static files
FROM node:16 as build-frontend

WORKDIR /app

# Ensure you copy over both the package.json and package-lock.json files
COPY streamlit_supabase_auth/frontend/package*.json ./
RUN npm install

# Copy the rest of your frontend app
COPY streamlit_supabase_auth/frontend/ ./
RUN npm run build

# Set up the Streamlit app
FROM python:3.10-alpine3.16

# Install system dependencies for Streamlit and supervisord
RUN apk add --no-cache \
    apache-arrow \
    py3-apache-arrow \
    py3-pandas \
    py3-psutil \
    py3-pillow \
    py3-pyzmq \
    py3-cffi \
    nginx \
    supervisor

# Set environment variables for Python
ENV PYTHONPATH=/usr/lib/python3.10/site-packages
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
ENV PIP_NO_CACHE_DIR=1

WORKDIR /app

# Copy the frontend build files
COPY --from=build-frontend /app/build /usr/share/nginx/html

# Copy the backend Streamlit app
COPY . .

# If setup.py is in the root directory, this will work, otherwise you need to specify the correct path
RUN pip install --no-cache-dir .

# Copy the nginx configuration template
COPY streamlit_supabase_auth/frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Prepare the supervisord configuration file
COPY supervisord.conf /etc/supervisord.conf

# Expose the ports Nginx and Streamlit will run on
EXPOSE 80
EXPOSE 8501

# Use supervisord to run both Nginx and Streamlit
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]

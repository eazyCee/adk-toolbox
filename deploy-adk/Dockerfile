#  Copyright 2025 Google LLC
 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
 
#       https://www.apache.org/licenses/LICENSE-2.0
 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.10-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN apt-get update && apt-get install -y libpq-dev
# RUN apt-get install -y postgresql-server-dev-all
RUN apt-get install -y build-essential
RUN pip install --no-cache-dir -r requirements.txt
# Service must listen to $PORT environment variable.
# This default is compatible with Cloud Run.
ENV PORT 8080

# Run the web server on container startup.
# Use gunicorn for production deployments. Install it first.
# RUN pip install gunicorn
RUN pip install gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
# Use 'flask run' for local development/debugging if needed, but gunicorn is recommended for Cloud Run
# CMD exec flask run --host=0.0.0.0 --port=$PORT

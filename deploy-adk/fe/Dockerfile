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

# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
# Cloud Run injects the PORT environment variable. We'll tell Streamlit
# to listen on this variable's value. 8080 is a common convention
# but the actual port comes from the environment variable.
EXPOSE 8080

# Run app.py when the container launches
# Pass the PORT environment variable to Streamlit
# --server.enableCORS false and --server.enableXsrfProtection false are often needed
# when deploying Streamlit in such environments. Adjust if you have specific security needs.
CMD ["streamlit", "run", "fe.py", "--server.port", "8080"]

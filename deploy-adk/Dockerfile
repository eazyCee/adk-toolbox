FROM python:3.11-slim

WORKDIR /app

# Copy files
COPY . /app

# Install production dependencies.
RUN apt-get update && apt-get install -y libpq-dev build-essential && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt

# Expose the A2A port
EXPOSE 8001

# Run the A2A agent (FastAPI) with Uvicorn
CMD ["uvicorn", "agent.agent:a2a_app", "--host", "0.0.0.0", "--port", "8001"]

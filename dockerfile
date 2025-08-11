FROM mcr.microsoft.com/playwright/python:v1.47.0-jammy

WORKDIR /app

# Copy all project files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install browsers (already present in base image, but ensure updated)
RUN playwright install

# Set environment variables
ENV CI=true

CMD ["pytest", "-v", "--env", "qa", "--maxfail=1", "--disable-warnings"]

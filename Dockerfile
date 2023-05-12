FROM python:3.10

# Set working directory
WORKDIR /app

# Copy requirements file to container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy bot script to container
COPY bot.py .

# Run bot script
CMD [ "python", "bot.py" ]

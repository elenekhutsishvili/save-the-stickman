# Use an official Python image as the base
FROM python:3.12

# Set the working directory in the container
WORKDIR /app
ENV FLASK_SECRET_KEY=stickman_secret_2025


# Copy all files from current directory to container's /app folder
COPY . .

# Install Python packages from requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose Flask's default port
EXPOSE 5000

# Run the app
CMD ["python3", "main.py"]
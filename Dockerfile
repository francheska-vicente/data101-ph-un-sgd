FROM python:3.8

# Working directory
WORKDIR /

# Copy requirements file and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose the server port
EXPOSE 8080

HEALTHCHECK CMD curl --fail http://localhost:8080 || exit 1

# Calculate the number of worker processes based on the number of CPU cores
CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:server"]
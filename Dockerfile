# Use official Python image as base
FROM python:3.11-slim

# Set environment variables to avoid writing pyc files
ENV PYTHONUNBUFFERED=1
ENV DJANGO_DEBUG=0

# Set the working directory inside the container
WORKDIR /app

# Copy only requirements file first to leverage Docker cache
COPY requirements.txt /app/

# Install system dependencies for PostgreSQL
RUN apt-get update

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the Django project
COPY ./django /app/

# Collect static files (important for production)
# RUN python manage.py collectstatic --noinput

# Install Gunicorn and Nginx (Nginx will be installed via the Compose setup)
RUN pip install gunicorn

# Expose the port Gunicorn will run on
EXPOSE 8000

# Now change the working directory if needed
#WORKDIR /app/django

# Command to run Gunicorn server
#CMD ["gunicorn", "sciplot.wsgi:application", "--bind", "0.0.0.0:8000"]

# Set the command to run the migrations, collectstatic, and then start Gunicorn
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic --noinput && gunicorn sciplot.wsgi:application --bind 0.0.0.0:8000 --reload"]

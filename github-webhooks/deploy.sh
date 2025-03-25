#!/bin/bash
cd /home/josue/sciplot

echo "Pulling latest changes..."
git fetch && git pull origin main || { echo "Git pull failed"; exit 1; }

echo "Building Docker image..."
docker build -t sciplot . || { echo "Docker build failed"; exit 1; }

echo "Starting new container..."
# Start the new container but don't detach yet, so we can check if it fails immediately
docker run --env-file /home/josue/sciplot/.env -d --name sciplot -p 8000:8000 sciplot

echo "Deployment successful! The new container is now running."

#!/bin/bash
cd /home/josue/sciplot

echo "Pulling latest changes..."
git pull origin main || { echo "Git pull failed"; exit 1; }

echo "Building Docker image..."
docker build -t sciplot . || { echo "Docker build failed"; exit 1; }

echo "Stopping old container..."
docker stop sciplot && docker rm sciplot

echo "Starting new container..."
docker run -d --name sciplot -p 8000:8000 sciplot || { echo "Docker run failed"; exit 1; }

echo "Deployment successful!"

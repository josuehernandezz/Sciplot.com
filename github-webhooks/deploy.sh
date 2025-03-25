#!/bin/bash
cd /home/josue/sciplot

echo "Pulling latest changes..."
git fetch && git pull origin main || { echo "Git pull failed"; exit 1; }

echo "Building Docker image..."
docker build -t sciplot . || { echo "Docker build failed"; exit 1; }


# Check if a container named 'sciplot' is already running
existing_container=$(docker ps -q -f name=sciplot)

if [[ -z "$existing_container" ]]; then
    echo "Starting new container..."
    docker run --env-file /home/josue/sciplot/.env -d --name sciplot -p 8000:8000 sciplot || { echo "Docker run failed"; exit 1; }
else
    echo "Stopping and removing existing container named 'sciplot'..."
    docker stop sciplot || { echo "Failed to stop existing container"; exit 1; }
    docker rm sciplot || { echo "Failed to remove existing container"; exit 1; }
fi

echo "Deployment successful! The new container is now running."

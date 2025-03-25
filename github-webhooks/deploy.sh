#!/bin/bash
cd /home/josue/sciplot

echo "Pulling latest changes..."
git fetch && git pull origin main || { echo "Git pull failed"; exit 1; }

echo "Building Docker image..."
docker build -t sciplot . || { echo "Docker build failed"; exit 1; }

echo "Starting new container..."
# Start the new container but don't detach yet, so we can check if it fails immediately
docker run --env-file /home/josue/sciplot/.env -d --name sciplot -p 8000:8000 sciplot
START_STATUS=$?

if [ $START_STATUS -ne 0 ]; then
    echo "Error: New Docker container failed to start. The existing container is still running."
    echo "Please check the logs of the new container to see what went wrong."
    echo "Run 'docker logs sciplot' to view the error messages."
    echo "You can also check the docker daemon logs for more details on the issue."

    # Provide some useful tips for troubleshooting
    echo "If the error is related to dependencies or the application, try the following:"
    echo "- Check the requirements.txt for missing dependencies."
    echo "- Check if the environment variables (if any) are correctly set."
    echo "- Make sure the ports are not being blocked by a firewall or other process."

    echo "Leaving old container running. Please fix the issue and try again."
    echo "Try running:"
    echo "docker logs sciplot"
    exit 1
fi

# If the new container starts successfully, stop the old one
# echo "Stopping old container..."
# docker stop sciplot && docker rm sciplot

echo "Deployment successful! The new container is now running."

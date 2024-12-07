#!/bin/bash

set -e

echo "Pulling Docker image..."
docker pull ghcr.io/j3rrryy/school_464:latest
docker tag ghcr.io/j3rrryy/school_464:latest school_464_django
docker rmi ghcr.io/j3rrryy/school_464:latest || true

echo "Starting services for certificate generation..."
docker compose -f docker-compose.cert.yml up -d

certbot_container=$(docker compose -f docker-compose.cert.yml ps -q certbot)
echo "Waiting for Certbot container to exit..."
docker wait "$certbot_container"

echo "Certbot logs:"
docker logs "$certbot_container"

echo "Stopping certificate services..."
docker compose -f docker-compose.cert.yml down

echo "Starting production build..."
docker compose -f docker-compose.prod.yml up -d

echo "Scheduling tasks for certificate renewal and cleanup..."
sudo chmod +x renew_cert.sh cleanup.sh
(crontab -l; echo "0 0 1 */2 * bash ./school_464/renew_cert.sh"; echo "0 0 * * * bash ./school_464/cleanup.sh") | crontab -

echo "Deployment complete!"

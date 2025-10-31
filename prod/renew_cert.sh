#!/bin/bash

cd ./school_464/
docker compose -f docker-compose.prod.yml stop nginx
docker compose -f docker-compose.cert.yml run --rm certbot renew
docker compose -f docker-compose.cert.yml down
docker compose -f docker-compose.prod.yml start nginx

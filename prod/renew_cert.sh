#!/bin/bash

cd ./school_464/
docker compose -f docker-compose.cert.yml run --rm -d certbot renew
docker compose -f docker-compose.prod.yml exec nginx nginx -s reload

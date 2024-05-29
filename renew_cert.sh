#!/bin/bash

cd ./school_464/
docker compose run --rm -d certbot renew
docker compose exec nginx nginx -s reload

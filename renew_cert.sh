#!/bin/bash

docker compose run --rm certbot renew --quiet
docker compose exec nginx nginx -s reload

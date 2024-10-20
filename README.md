# School website

<p align="center">
  <img src="https://github.com/j3rrryy/school_464/actions/workflows/main.yml/badge.svg">
  <a href="https://codecov.io/gh/j3rrryy/school_464">
    <img src="https://codecov.io/gh/j3rrryy/school_464/graph/badge.svg?token=5SP4EMB1B3"/>
  </a>
  <a href="https://www.python.org/downloads/release/python-3120/">
    <img src="https://img.shields.io/badge/Python-3.12-FFD64E.svg" alt="Python 3.12">
  </a>
  <a href="https://github.com/j3rrryy/school_464/blob/main/LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="MIT License">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Black formatter">
  </a>
</p>

## :book: Key features

- RSS
- PWA
- Dynamic menu
- Dynamic footer
- Uses PostgreSQL
- Supports XML maps
- Custom error pages
- Supports caching (Redis)
- Easy editing of HTML pages
- Version for the visually impaired
- Automatic conversion of images to WebP
- Automatic cleaning of unused media files

## :computer: Requirements

- Docker

## :hammer_and_wrench: Getting started

- Copy `.env.dev` file from `examples/docker/env/` to `docker/env/` folder fill it in

- **(For prod)** Copy `.env.prod` file from `examples/docker/env/` to `docker/env/` folder and fill it in

- **(For prod)** Copy `django.conf` file from `examples/docker/nginx/prod/` to `docker/nginx/prod` folder and fill it in

- **(For prod)** Copy `docker-compose.yml` file from `examples/` to `/` folder and fill it in

### :rocket: Start

- Run the **dev build**

  ```shell
  docker compose -f docker-compose.dev.yml up --build -d
  ```

- Run the **prod build** and get a SSL certificate

  - Build the project

    ```shell
    docker compose build
    ```

  - Start Docker and get a certificate

    ```shell
    docker compose up nginx certbot
    ```

  - Stop your containers to continue

    ```shell
    docker compose stop
    ```

  - Comment out the command in `docker-compose.yml`

    ```shell
    command: certonly --webroot --webroot-path=/var/www/certbot/ --email <your_email> --agree-tos --no-eff-email -d <domain (example.com)> -d <domain (www.example.com)>
    ```

  - Uncomment the part of nginx config in `docker/nginx/prod/django.conf`

  - Start Docker again

    ```shell
    docker compose up -d
    ```

  - Run the setup script

    ```shell
    bash setup.sh
    ```

### :construction_worker: Maintenance

- Create superuser

  - Get access to the container

     ```shell
    docker exec -it <container_name> sh
    ```

  - Press `Ctrl+C` + `Ctrl+Shift+V`

    ```shell
    python manage.py createsuperuser
    ```

---

- Run tests

  - Get access to the container

     ```shell
    docker exec -it <container_name> sh
    ```

  - Press `Ctrl+C` + `Ctrl+Shift+V`

    ```shell
    python manage.py test
    ```

### :x: Stop

```shell
docker compose stop
```

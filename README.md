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
  <a href="https://github.com/astral-sh/ruff">
    <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json" alt="Ruff">
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

- Copy `.env` file from `examples/dev/` to `dev/` folder fill it in

- **(For prod)** Copy `.env` file from `examples/prod/` to `prod/` folder and fill it in

- **(For prod)** Copy `nginx.conf` file from `examples/prod/` to `prod/` folder and fill it in

- **(For prod)** Copy `docker-compose.cert.yml` file from `examples/prod/` to `prod/` folder and fill it in

### :rocket: Start

- Run the **dev build**

  ```shell
  docker compose -f docker-compose.dev.yml up --build -d
  ```

- Run the **prod build** and get a SSL certificate

  - Create the directory on the server

    ```shell
    mkdir -p /school_464/
    ```

  - Use SCP to copy the prod files to the server

    ```shell
    scp -r ./prod/* <username>@<host>:/school_464/
    ```

  - Pull the Docker image from the GitHub Container Registry

    ```shell
    docker pull ghcr.io/j3rrryy/school_464:latest
    docker tag ghcr.io/j3rrryy/school_464:latest school_464_django
    ```

  - Start the services to get a certificate

    ```shell
    docker compose -f docker-compose.cert.yml up
    ```

  - Stop the services

    ```shell
    docker compose down
    ```

  - Start the prod build

    ```shell
    docker compose -f docker-compose.prod.yml up -d
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

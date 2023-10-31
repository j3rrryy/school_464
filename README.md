# School website

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

- Create `.env.dev` file with variables as in the file in the `examples/docker/env/` folder, then put it in the `docker/env/` folder

- **(For prod)** Create `.env.prod` file with variables as in the file in the `examples/docker/env/` folder, then put it in the `docker/env/` folder

- **(For prod)** Create `django.conf` file with your data as in the `examples/docker/nginx/prod/` folder, then put it in the `docker/nginx/prod` folder

- **(For prod)** Create `docker-compose.yml` file with your data as in the `examples/` folder, then put it in the `/` folder

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
    python manage.py test main
    ```

### :x: Stop

```shell
docker compose stop
```

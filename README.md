# School website

## :book: Key features

- Easy editing of HTML pages
- Dynamic menu
- Dynamic footer
- Automatic cleaning of unused media files
- Automatic conversion of images to WebP
- Automatic DB backups (Celery)
- Uses PostgreSQL
- Supports caching (Redis)
- Supports XML maps
- Custom error pages
- Version for the visually impaired

## :computer: Requirements

- Docker

## :hammer_and_wrench: Getting started

- Create `.env.dev` file with variables as in the file in the `examples/docker/env/` folder, then put it in the `docker/env/` folder

- **(For prod)** Create `.env.prod` file with variables as in the file in the `examples/docker/env/` folder, then put it in the `docker/env/` folder

- **(For prod)** Create `django.conf` file with your data as in the `examples/docker/nginx/prod/` folder, then put it in the `docker/nginx/prod` folder

- **(For prod)** Create `docker-compose.yml` file with your data as in the `examples/` folder, then put it in the `/` folder

- **(For prod)** Change `settings.py`: `environ.Env.read_env(env_file=Path('./docker/env/.env.dev'))` ---> `environ.Env.read_env(env_file=Path('./docker/env/.env.prod'))`

### :rocket: Start

- Run the **dev build**

    ```shell
    docker compose -f docker-compose.dev.yml up --build -d
    ```

- Run the **prod build** and get an SSL certificate

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
    # certonly --webroot --webroot-path=/var/www/certbot/ --email email@mail.com --agree-tos --no-eff-email -d example.com -d www.example.com
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

- Create a database backup file

  - Get access to the container

     ```shell
    docker exec -it <container_name> sh
    ```

  - Press `Ctrl+C` + `Ctrl+Shift+V`

    ```shell
    python manage.py dumpdata --exclude auth.permission --exclude contenttypes > backup/<your_file_name>.json
    ```

---

- Restore the database from backup files

  - Get access to the container

     ```shell
    docker exec -it <container_name> sh
    ```

  - Press `Ctrl+C` + `Ctrl+Shift+V`

    ```shell
    python manage.py loaddata backup/<your_file_name>.json
    ```

### :x: Stop

```shell
docker compose stop
```

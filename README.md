# lms-back

Project build and up
```bash
docker-compose up -d --build
```

Make migrations
```bash
docker-compose run admin poetry run python3 manage.py makemigrations
docker-compose run admin poetry run python3 manage.py migrate
```
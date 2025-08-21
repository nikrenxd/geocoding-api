## Geocoding API


### Copy .env file
Create .env file and enter your API key and DB URL
```shell
    mv .env.example .env
```

### Run project
Run project via docker compose
```shell
    docker compose up
```

### Applying migrations
Create tables before using project
```shell
  docker compose exec web uv run alembic upgrade head    
```



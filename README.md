# Geocoding API


## Stack
| Tool                  | Role                                |
|-----------------------|-------------------------------------|
| **FastAPI**           | Async REST framework                |
| **SQLAlchemy**        | ORM for working with DB             |
| **Taskiq + RabbitMQ** | Async task queue and message broker |
| **PostgreSQL**        | Data storage                        |
| **Redis**             | Taskiq result backend               |

## Project setup
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

## Endpoints
### /api/geocode/coords
#### Convert coordinates to location name
#### Get location name from location coordinates
```bash
curl -X 'GET' \
  'http://<YOUR_DOMAIN>:<YOUR_PORT>/api/geocode/coords?latitude=52.5170365&longitude=13.3888599' \
  -H 'accept: application/json'
```
#### Response
```json
{
  "created_at": "2025-10-15T15:24:05.419479Z",
  "display_name": "Berlin, Germany"
}
```

### /api/geocode/location
#### Request
#### Get location coordinates from location name
```bash
curl -X 'GET' \
  'http://<YOUR_DOMAIN>:<YOUR_PORT>/api/geocode/location?query_location=Berlin' \
  -H 'accept: application/json'
```
#### Response
```json
{
  "created_at": "2025-10-15T15:31:10.933976Z",
  "display_name": "Berlin, Germany",
  "lat": 52.5170365,
  "lon": 13.3888599
}
```


# TODO Web App

A containerized web application with Redis caching and PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose

## Starting the Application

To start the entire application stack:

```bash
docker-compose up -d
```

This will start three services:
- **todowebapp**: The main web application (accessible on port 80)
- **redis**: Redis cache server
- **postgres**: PostgreSQL database

The `-d` flag runs the containers in detached mode (in the background).

## Stopping the Application

To stop all services while preserving data:

```bash
docker-compose down
```

This stops and removes the containers but keeps the data volumes intact.

## Restarting the Application

To restart the application with existing data:

```bash
docker-compose down
docker-compose up -d
```

Or simply:

```bash
docker-compose restart
```

## Data Persistence

Your data is automatically preserved in Docker volumes:
- `redis_data_todo`: Redis data
- `postgres_data_todo`: PostgreSQL database

These volumes persist even when containers are stopped or removed.

## Accessing the Application

- Web App: http://0.0.0.0

## Complete Cleanup (⚠️ Destroys Data)

To remove everything including data volumes:

```bash
docker-compose down -v
```

**Warning**: This will permanently delete all application data.

## Troubleshooting

If you encounter issues:

1. Check container status: `docker-compose ps`
2. View logs: `docker-compose logs [service-name]`
3. Rebuild if needed: `docker-compose up --build`
4. View docker container information: `docker ps`

## Database Credentials

- Database: `webservice_db_postgres`
- Username: `postgres`
- Password: `password`

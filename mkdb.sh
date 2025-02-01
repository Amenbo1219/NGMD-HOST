docker compose up -d --build 
sleep 2
docker exec -it postgres_db psql -U postgres -d monitoring -f /docker-entrypoint-initdb.d/init-db.sql

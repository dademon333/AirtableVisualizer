FROM postgres:14-alpine
COPY trgm.sql /docker-entrypoint-initdb.d
EXPOSE 5432
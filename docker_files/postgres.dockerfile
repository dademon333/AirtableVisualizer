FROM postgres:15.1-alpine
COPY trgm.sql /docker-entrypoint-initdb.d
EXPOSE 5432
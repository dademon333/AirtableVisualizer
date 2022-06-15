ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}_graph_front as graph
FROM ${COMPOSE_PROJECT_NAME}_table_front as table

FROM python:3.10-alpine

WORKDIR /usr/src/app

RUN apk add --no-cache build-base
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY --from=graph /frontend/build/index.html /frontend/graph/build/index.html
COPY --from=table /frontend/build/index.html /frontend/table/build/index.html

COPY . .

EXPOSE 8080
ENTRYPOINT ["gunicorn", "main:app"]
CMD ["-c", "gunicorn_config.py"]

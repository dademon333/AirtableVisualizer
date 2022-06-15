ARG COMPOSE_PROJECT_NAME
FROM ${COMPOSE_PROJECT_NAME}_graph_front as graph
FROM ${COMPOSE_PROJECT_NAME}_table_front as table

FROM nginx:1.21-alpine

COPY --from=graph /frontend/build/static /frontend/build/static
COPY --from=table /frontend/build/static /frontend/build/static

COPY ./nginx.conf /etc/nginx/nginx.conf

ENTRYPOINT ["nginx", "-g", "daemon off;"]
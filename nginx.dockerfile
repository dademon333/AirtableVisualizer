FROM node:18-alpine AS graph
WORKDIR /frontend/

COPY frontend/graph/package.json .
RUN npm install --only=prod

COPY frontend/graph .
RUN npm run build



FROM node:18-alpine AS table
WORKDIR /frontend/

COPY frontend/table/package.json .
RUN npm install --only=prod

COPY frontend/table .
RUN npm run build



FROM nginx:1.23.0-alpine

COPY docker_files/nginx.conf /etc/nginx/nginx.conf
COPY --from=graph /frontend/build /frontend/graph
COPY --from=table /frontend/build /frontend/table

ENTRYPOINT ["nginx", "-g", "daemon off;"]
FROM node:18-alpine

WORKDIR /usr/src/app/frontend/table/

COPY package.json .
RUN npm install --only=prod

COPY . .
RUN npm run build
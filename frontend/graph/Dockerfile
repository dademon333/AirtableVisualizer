FROM node:18-alpine

WORKDIR /usr/src/app/frontend/graph/

COPY package.json .
RUN npm install --only=prod

COPY . .
RUN npm run build
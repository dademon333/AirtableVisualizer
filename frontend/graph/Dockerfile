FROM node:18-alpine

WORKDIR /frontend/

COPY package.json .
RUN npm install --only=prod

COPY . .
RUN npm run build
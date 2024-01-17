# Dockerfile - FrontEnd Vue.js

# Etape de construction
FROM node:14 AS build-stage
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run serve

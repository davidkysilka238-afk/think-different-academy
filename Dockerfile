FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY index.html ./
COPY src ./src
RUN npm run build

FROM python:3.13-slim

WORKDIR /app
COPY server.py schema.sql LICENSE ./
COPY --from=build /app/dist ./dist

ENV PORT=80
EXPOSE 80

CMD ["python", "server.py"]

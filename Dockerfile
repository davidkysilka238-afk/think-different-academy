FROM node:22-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY index.html ./
COPY src ./src
RUN npm run build

FROM python:3.13-slim

WORKDIR /app
COPY server.py schema.sql ./
COPY --from=build /app/dist ./dist
RUN python -c "import sqlite3; database = sqlite3.connect('team.db'); database.executescript(open('schema.sql', encoding='utf-8').read()); database.close()"

ENV PORT=80
EXPOSE 80

CMD ["python", "server.py"]

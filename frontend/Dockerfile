# --- Build stage ---
FROM node:20-alpine AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .

# Valor por defecto: apuntamos a /api para usar el proxy de Nginx
ARG VITE_API_BASE_URL=/api
ENV VITE_API_BASE_URL=${VITE_API_BASE_URL}

RUN npm run build

# --- Runtime stage ---
FROM nginx:alpine
# Config de Nginx con proxy a la API y fallback para SPA
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
# Archivos estáticos de Vite
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

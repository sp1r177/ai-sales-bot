FROM node:20-alpine AS build
WORKDIR /app

# Install deps
COPY client/package.json client/package-lock.json* /app/
RUN npm ci || npm install

# Build
COPY client /app
ARG VITE_API_BASE
ENV VITE_API_BASE=${VITE_API_BASE}
RUN npm run build

# runtime is provided by nginx; keep dist in volume via compose
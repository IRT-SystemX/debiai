# DebiAI Vuejs Frontend
FROM node:lts-alpine as build-stage
WORKDIR /frontend
COPY frontend/ .
ENV NODE_OPTIONS="--openssl-legacy-provider"
RUN npm install
RUN npm run build

# DebiAI Python Backend
FROM python:3.8-slim-buster
WORKDIR /backend
COPY backend/ .
RUN pip install --trusted-host pypi.python.org -r requirements.txt
COPY --from=build-stage /frontend/dist dist
ENV FLASK_ENV production
CMD ["python", "websrv.py"]


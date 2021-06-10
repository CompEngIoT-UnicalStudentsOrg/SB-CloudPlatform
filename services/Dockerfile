FROM nodered/node-red:latest

COPY backend_flow.json /data/backend_flow.json

ENV FLOWS=backend_flow.json
RUN npm install node-red-contrib-redis

EXPOSE 1880
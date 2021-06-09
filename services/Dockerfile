FROM nodered/node-red:latest

ENV FLOWS=backend_flow.json
RUN npm install node-red-contrib-redis && npm i --unsafe-perm node-red-node-sqlite

EXPOSE 1880
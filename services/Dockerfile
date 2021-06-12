FROM nodered/node-red:latest

COPY flows.json /data/flows.json
RUN npm install node-red-contrib-redis

EXPOSE 1880
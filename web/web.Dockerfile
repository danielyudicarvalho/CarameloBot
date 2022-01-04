FROM node:14
COPY . /var/www
WORKDIR /var/www
RUN npm install
ENTRYPOINT ["node", "server.js"]
ENV PORT=8080
EXPOSE $PORT
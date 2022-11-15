FROM node:19.1-alpine AS build

WORKDIR /app

COPY front/package.json front/package-lock.json /app/
RUN npm install

COPY front/ .

RUN npm run build

FROM nginx:latest

COPY --from=build /app/dist /srv/www/clikodrome

RUN rm /etc/nginx/conf.d/default.conf
COPY --from=build /app/nginx/default.conf /etc/nginx/conf.d/default.conf
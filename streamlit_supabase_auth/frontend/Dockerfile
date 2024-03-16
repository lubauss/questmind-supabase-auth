# syntax = docker/dockerfile:1

ARG NODE_VERSION=16
FROM node:${NODE_VERSION}-slim as base

LABEL fly_launch_runtime="Node.js"
WORKDIR /app
ENV NODE_ENV="production"

FROM base as build

RUN apt-get update -qq && \
    apt-get install --no-install-recommends -y build-essential node-gyp pkg-config

COPY --link package-lock.json package.json ./
RUN npm ci

COPY --link . .
RUN npm run build

FROM base

COPY --from=build /app /app

EXPOSE 3000
CMD [ "npm", "run", "start" ]

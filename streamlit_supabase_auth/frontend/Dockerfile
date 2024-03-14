FROM node:16 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . ./
RUN npm run build

# Use Nginx to serve the React build
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html

# Copy the default nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

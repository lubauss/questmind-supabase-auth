FROM node:16 as build

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . ./
RUN npm run build

# Use Nginx to serve the React build
FROM nginx:stable-alpine

# Copy the React build from the previous stage
COPY --from=build /app/build /usr/share/nginx/html

# Create a template file for envsubst
# Rename the original nginx.conf to default.conf.template
COPY nginx.conf /etc/nginx/conf.d/default.conf.template

EXPOSE 80

# Use a shell form of CMD so that envsubst can be run before Nginx starts
CMD ["nginx", "-g", "daemon off;"]


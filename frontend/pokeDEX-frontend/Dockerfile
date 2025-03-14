# Build stage
FROM node:20-slim AS build

# Install dependencies for ChromeHeadless (for testing)
RUN apt-get update && apt-get install -y \
  wget \
  gnupg \
  && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update && apt-get install -y \
  google-chrome-stable \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci
RUN npm install -g @angular/cli

# Copy the rest of the application code
COPY . .

# Build the Angular app
RUN npm run build -- --configuration production

# Serve stage
FROM nginx:alpine

# Copy the built files from the build stage to the Nginx directory
COPY --from=build /app/dist/poke-dex-frontend /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
FROM node:20-alpine

WORKDIR /app

# Copy package files for dependency installation
COPY package*.json ./

# Install dependencies
RUN npm install

# Provide build-time argument for API URL, and set as environment variable so CRA can access
ARG REACT_APP_API_URL
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Copy the rest of the app
COPY . .

# Build the React app with the API URL embedded
RUN npm run build

# Install serve to run the built app
RUN npm install -g serve

# Expose port 3000
EXPOSE 3000

# Command to run the app
CMD ["serve", "-s", "build", "-l", "3000"]
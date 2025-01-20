# Stage 1: Build the application
FROM node:18-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install production dependencies and dev dependencies for build
RUN npm install -g pnpm
RUN pnpm install

# Copy the entire application code
COPY . .

RUN rm -f .env
RUN mv .env.docker .env

# Generate Prisma Client
RUN pnpx prisma generate

# Build the Next.js application
RUN pnpm run build

# Stage 2: Run the application in production mode
FROM node:18-alpine AS runner

# Set NODE_ENV to production
ENV NODE_ENV=production

# Set working directory
WORKDIR /app

# Copy the production build and dependencies from the builder stage
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/prisma ./prisma

RUN npm install -g pnpm

# Set Prisma to look for migrations
#ENV DATABASE_URL=postgresql://your_user:your_password@db:5432/your_database

# Expose the port used by the app
EXPOSE 3000

# Start the application
CMD ["pnpm", "run", "start"]

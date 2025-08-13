FROM node:20-alpine

WORKDIR /app

COPY app/package.json app/package-lock.json ./

RUN npm ci

COPY app/ ./

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "3000"]


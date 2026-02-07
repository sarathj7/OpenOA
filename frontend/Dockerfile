FROM node:20-alpine AS deps
WORKDIR /app
COPY frontend/package.json ./package.json
RUN npm install --legacy-peer-deps


FROM node:20-alpine AS builder
WORKDIR /app

# ---- ADD THESE TWO LINES ----
ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
# -----------------------------

COPY --from=deps /app/node_modules ./node_modules
COPY frontend/ ./

RUN npm run build || (cat .next/trace && exit 1)


FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/next.config.mjs ./next.config.mjs

EXPOSE 3000
CMD ["npm", "run", "start"]

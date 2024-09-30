FROM node:20.17-bookworm

WORKDIR /app
COPY ./webapp .

RUN npm i -g pnpm
RUN pnpm i

CMD [ "pnpm", "dev" ]
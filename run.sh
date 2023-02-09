#!/bin/bash -ex

NAME=itilbot

docker build -t ${NAME} .
docker rm -f ${NAME} || true
docker run --name ${NAME} -d --restart=unless-stopped -e ITIL_BOT_TOKEN=${ITIL_BOT_TOKEN}  ${NAME}
docker logs -f ${NAME}

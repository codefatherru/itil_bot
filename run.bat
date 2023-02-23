

set ITIL_BOT_TOKEN=%1

set DOCKER_NAME=itilbot

docker build -t %DOCKER_NAME% .
docker rm -f %DOCKER_NAME% || true
docker run --name %DOCKER_NAME% -d --restart=unless-stopped -e ITIL_BOT_TOKEN=%ITIL_BOT_TOKEN% -e PYTHONUNBUFFERED=1  %DOCKER_NAME%
docker logs -f %DOCKER_NAME%

pause
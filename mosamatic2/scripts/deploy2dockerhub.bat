@echo off

FOR /F %%v IN ('poetry version --short') DO SET VERSION=%%v
echo Deploying version %VERSION% to DockerHub...
set /p CONFIRM="Is this correct? (y/n) "
if /I NOT "%CONFIRM%"=="y" (
    echo Aborting deployment
    exit /b 1
)

docker logout
type C:\\Users\\r.brecheisen\\dockerhub.txt | docker login --username brecheisen --password-stdin
docker push brecheisen/mosamatic2-cli:%VERSION%

echo "Make sure to set the Docker repository to PUBLIC!!"
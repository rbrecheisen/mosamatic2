@echo off

FOR /F %%v IN ('poetry version --short') DO SET VERSION=%%v
docker build --no-cache -t brecheisen/mosamatic2-cli:%VERSION% .
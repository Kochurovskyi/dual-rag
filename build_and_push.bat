@echo off
REM Build and push Docker image to Docker Hub

set IMAGE_NAME=kochurovskyi/dual-rag
set VERSION=%1
if "%VERSION%"=="" set VERSION=latest

echo Building Docker image: %IMAGE_NAME%:%VERSION%
docker build -t %IMAGE_NAME%:%VERSION% .

echo Tagging as latest
docker tag %IMAGE_NAME%:%VERSION% %IMAGE_NAME%:latest

echo Pushing to Docker Hub...
docker push %IMAGE_NAME%:%VERSION%
docker push %IMAGE_NAME%:latest

echo Successfully pushed %IMAGE_NAME%:%VERSION% and %IMAGE_NAME%:latest to Docker Hub


#!/bin/bash

set -e

export IMAGE_NAME="vignet-app-frontend-react"

docker build -t $IMAGE_NAME -f Dockerfile .
docker run --rm --name $IMAGE_NAME -ti -p 3000:80 $IMAGE_NAME
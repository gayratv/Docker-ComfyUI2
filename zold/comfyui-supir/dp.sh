#!/bin/bash

echo "docker push gayrat/$IMAGE_NAME:$VERSION_PUSH"
echo "docker push gayrat/$IMAGE_NAME:$VERSION"
#docker tag "$IMAGE_NAME:$VERSION" gayrat/"$IMAGE_NAME:$VERSION_PUSH"
docker tag "$IMAGE_NAME:$VERSION" gayrat/"$IMAGE_NAME:$VERSION"
#docker push gayrat/"$IMAGE_NAME:$VERSION_PUSH"
docker push gayrat/"$IMAGE_NAME:$VERSION"
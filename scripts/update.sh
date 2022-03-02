#!/bin/bash

docker stop adhelp || true
docker rm adhelp || true
docker run -d --network=host -e LOAD_MODEL_STARTUP=1 --name adhelp --restart=always ad_help

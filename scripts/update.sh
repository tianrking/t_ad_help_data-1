#!/bin/bash

docker stop adhelp || true
docker rm adhelp || true
docker run -d --network=host --name adhelp --restart=always ad_help

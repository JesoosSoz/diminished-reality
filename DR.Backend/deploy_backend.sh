#!/bin/bash

# author: Fabian Wilhelm

set -e

cleanup () {
	echo "ERROR: $1 not found"
	rm -r ./backend
	exit 1
}

mkdir -p ./backend/volume || (echo "ERROR: creating backend folder failed" && exit 1) 

cp ./mobileFlask.py ./backend/volume/ || cleanup "docker-compose.yml"
cp ./docker-compose.yml ./backend || cleanup "docker-compose.yml"
cp ./Dockerfile ./backend/volume/ || cleanup "Dockerfile"
cp ./requirements.txt ./backend/volume/ || cleanup "requirements.txt"
cp -r ./ai ./backend/volume/ || cleanup "ai files"
cp -r ./configs ./backend/volume/|| cleanup "configs files"

cat << EOF && exit 0

>>> backend folder successfully created

to host this application on your server, follow these steps:

	1) copy the "backend" folder to your server
	2) install docker and docker-compose on your server
	3) open port 5000 for incoming connections
	4) change to the "backend" folder on your server
	5) run the command "docker-compose up" (you may need root permissions)
	
EOF

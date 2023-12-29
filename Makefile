build:
	docker build . --tag my_project
up:
	docker-compose -f ./docker-compose-local.yaml up -d
down:
	docker-compose -f ./docker-compose-local.yaml down && docker network prune --force

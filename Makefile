docker_dev := docker compose -f dev.docker-compose.yml
docker_deploy := docker compose -f deploy.docker-compose.yml

docker_dev_run := $(docker_dev) run --rm backend
docker_deploy_run := $(docker_deploy) run --rm backend

hello:
	echo "Hello, world!"

generate:
	$(docker_dev_run) alembic revision --autogenerate -m $(name)

migrate:
	$(docker_dev_run) alembic upgrade head

d_generate:
	$(docker_deploy_run) alembic revision --autogenerate -m $(name)

d_migrate:
	$(docker_deploy_run) alembic upgrade head

dev:
	$(docker_dev_run) up -d --build

deploy:
	$(docker_deploy_run) up -d --build

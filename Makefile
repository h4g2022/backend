docker_run := docker compose run --rm backend

hello:
	echo "Hello, world!"

generate:
	$(docker_backend) alembic revision --autogenerate -m $(name)

migrate:
	$(docker_backend) alembic upgrade head

dev:
	docker compose up -f dev.docker-compose.yml -d --build

deploy:
	docker compose up -f deploy.docker-compose.yml -d --build
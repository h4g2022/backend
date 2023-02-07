docker_run := docker compose run --rm backend

hello:
	echo "Hello, world!"

generate:
	$(docker_backend) alembic revision --autogenerate -m $(name)

migrate:
	$(docker_backend) alembic upgrade head

dev:
	docker compose -f dev.docker-compose.yml up -d --build

deploy:
	docker compose -f deploy.docker-compose.yml up -d --build

docker_run := docker compose run --rm backend

hello:
	echo "Hello, world!"

generate:
	$(docker_backend) alembic revision --autogenerate -m $(name)

migrate:
	$(docker_backend) alembic upgrade head

run:
	docker compose up -d --build
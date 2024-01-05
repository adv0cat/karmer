.PHONY: run-db-docker

include .env

run-db-docker:
	docker run --name postgres-db-client --rm \
		-p 5432:5432 \
		-v $$PWD/__postgres:/var/lib/postgresql/data \
		-v $$PWD/sql/init.sql:/docker-entrypoint-initdb.d/init.sql \
		-e POSTGRES_USER=${POSTGRES_USER} \
		-e POSTGRES_PASSWORD=${POSTGRES_PASSWORD} \
		-e POSTGRES_DB=${POSTGRES_DB} \
		-d postgres:alpine
	@echo "Postgres started"
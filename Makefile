dc-build:
	docker-compose up -d --build

dc-run:
	docker-compose up -d

dc-down:
	docker-compose down -v

dc-stop:
	docker-compose stop

d-run:
	docker run -d -p 8000:8000 --rm --name app

d-stop:
	docker stop


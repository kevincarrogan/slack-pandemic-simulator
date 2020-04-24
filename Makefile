up:
		docker-compose -f docker-dev-compose.yml up --build -d

build:
		docker-compose -f docker-dev-compose.yml build

test-services-slack:
		docker-compose -f docker-dev-compose.yml run --rm services-slack python manage.py test

make-migrations-services-slack:
		docker-compose -f docker-dev-compose.yml run --rm services-slack python manage.py makemigrations

migrate-services-slack:
		docker-compose -f docker-dev-compose.yml run --rm services-slack python manage.py migrate

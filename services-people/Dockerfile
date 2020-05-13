FROM python:3.8
RUN mkdir /var/www
WORKDIR /var/www
COPY requirements requirements
RUN pip install -r requirements/prod.txt
COPY . .
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

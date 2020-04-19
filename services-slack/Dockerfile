FROM python:3.8
RUN mkdir /var/www
WORKDIR /var/www
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY . .
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]

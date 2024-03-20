python3 -m venv venv
source venv/bin/activate
python -m pip install django
python -m pip freeze > requirements.txt
django-admin startproject FlashX .
python manage.py startapp ManageAPI
python -m pip install djangorestframework
python -m pip install psycopg2-binary


rm -rf ManageAPI/migrations
python manage.py makemigrations ManageAPI
python manage.py migrate

python manage.py createsuperuser
superuser/pass

python manage.py runserver


docker build -t flashx_backend .

docker images | grep flashx_backend

aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 378874850750.dkr.ecr.us-east-1.amazonaws.com

docker tag flashx_backend:latest 378874850750.dkr.ecr.us-east-1.amazonaws.com/flashx_backend:latest

docker push 378874850750.dkr.ecr.us-east-1.amazonaws.com/flashx_backend:latest

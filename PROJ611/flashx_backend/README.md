python3 -m venv venv
source venv/bin/activate
python -m pip install django
python -m pip freeze > requirements.txt
django-admin startproject FlashX .
python manage.py startapp ManageAPI
python -m pip install djangorestframework
python -m pip install psycopg2-binary


CREATE DATABASE flashx;

INSERT INTO auth_group (id,name) 
VALUES (1, 'admin');

INSERT INTO auth_group (id,name) 
VALUES (2, 'owner');

INSERT INTO auth_group (id,name) 
VALUES (3, 'staff');

INSERT INTO auth_group (id,name) 
VALUES (4, 'delivery');


python manage.py makemigrations
python manage.py migrate

python manage.py createsuperuser
superuser/pass

python manage.py runserver
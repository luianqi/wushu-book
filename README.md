
# Wushu Book

# Built With

> ### `Django` 
> ### `Django Rest Framework`
> ### `Django Channels`
> ### `PostgreSQL` 
> ### `Redis`
> ### `Nginx`

# Deployed to Heroku

### [Heroku](https://wushu-federation1.herokuapp.com/)

---
# Getting started
---
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
# Prerequisites
This is a project written using Python, Django and Django Rest Framework
1. Clone the repository
```
https://github.com/luianqi/wushu-book
```
2. Create the virtual enviroment
 ```
python3 -m venv venv
source venv/bin/activate
```
3. Install the requirements
```
pip install -r requirements.txt
```
4. Create a new PostgreSQL database

In your terminal:
```
psql postgres
CREATE DATABASE databasename
\c databasename
```
5. Build the Docker Image
```
$ docker-compose build 
```
6. Create a new superuser
```
$ docker-compose run --rm app_name python manage.py createsuperuser
```
9. Run the project
```
$ docker-compose up
```

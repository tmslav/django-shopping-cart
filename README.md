# Django add to external shopping cart application
##Requirements:

### Basic instalation
- [redis server](http://redis.io/)
- [memcached](http://memcached.org/)
- [rabbit-mq](https://www.rabbitmq.com/)
### Pip installation
```pip -r requirements.txt```

 
###Django settings
 ```
 INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'rest_framework',
    'shop_api',
    'ipware'
)
```
Add this for CELERY configuration

```
CELERY_RESULT_BACKEND = 'cache+memcached://127.0.0.1:11211/'
CELERY_CACHE_BACKEND = 'memory'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_IGNORE_RESULT = False
```


### Running
- pull the project to Your project and copy the src/celery file to Your Django configuration folder.
- add the urls to Your urls file
- run migrations to save to the database and create tables
```./migrate.py makemigrations```
```./migrate.py migrate```

- configure and run redis, rabbit-mq and memcached, in deamon mode or normal mode
- start celery workers
- worker that makes requests to websites ( run more to start more workers) 
```celery -A src worker```
- worker to clean memcached
```celery -A src beat```






### Lähtekoodi allalaadimine koodihoidlast  

```bash
git clone git@github.com:emmakuppart/toyrem-api.git
```

### Pip alla laadimine

```bash
python3 -m pip install --user --upgrade pip
```

### Virtuaalse keskkonna alla laadimine

```bash
python3 -m pip install --user virtualenv
```

### Virtuaalse keskkonna loomine

```bash
python3 -m venv env
```

### Virtuaalse keskkonna aktiveerimine & deaktiveerimine

```bash
source env/bin/activate
```

```bash
deactivate
```

### Django alla laadimine (virtuaalses keskkonnas)

```
pip install django
pip install djangorestframework
pip install psycopg2 (Postgres andmebaas)
python -m pip install Pillow (piltide haldus)
pip install django-cors-headers (Päringuvõltsingu kaitse)
pip install pymemcache (sessioonid)
pip install django-apscheduler (taustaprotsessid)
```

### Rakenduse käivitamine (vaikimisi port 8000)

```
python manage.py runserver
```

### Andmebaasi uuendamine

```
python manage.py makemigrations
python manage.py migrate api --run-syncdb --fake
```

### Admin kasutaja loomine

```
python manage.py createsuperuser
```

### Andmebaasi loomine

```
docker-compose up
```

### Kasutatud materjalid

```
https://medium.com/swlh/build-your-first-rest-api-with-django-rest-framework-e394e39a482c
https://bezkoder.com/django-rest-api/
https://docs.djangoproject.com/en/3.2/topics/http/sessions/
```
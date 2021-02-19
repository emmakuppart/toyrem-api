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
```

### Rakenduse käivitamine (vaikimisi port 8000)

```
python manage.py runserver
```

### Andmebaasi uuendamine

```
python manage.py migrate
```

### Admin kasutaja loomine

```
python manage.py createsuperuser
```

# VAMTIGER User Registry [Django](https://www.djangoproject.com)
A behaviour driven [Django](https://www.djangoproject.com) demo api for usage with the Custom Element [vamtiger-user-registry-web-component](https://github.com/vamtiger-project/vamtiger-user-registry-web-component/tree/source).

## Installation
```bash
pip install -r requirements.txt
```

## Testing
Automated behaviour driven tests were implemented with [behave-django](https://behave-django.readthedocs.io/en/stable/), and can be run as follows:
```sh
python manage.py behave
```

For test coverage:
```sh
coverage erase
coverage run manage.py behave
coverage report
```
or
```bash
sh test.sh
```
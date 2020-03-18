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
<img src=https://raw.githubusercontent.com/vamtiger-project/vamtiger-user-registry-django/master/image/bdd-tests.jpg style="max-height: 500px; background-color: #f0f0f0; border-radius: 3px" width=400>

For test [coverage](https://coverage.readthedocs.io/en/coverage-5.0.4/):
```sh
coverage erase
coverage run manage.py behave
coverage report
```
or
```bash
sh test.sh
```
<img src=https://raw.githubusercontent.com/vamtiger-project/vamtiger-user-registry-django/master/image/test-coverage.jpg style="max-height: 350px; background-color: #f0f0f0; border-radius: 3px" width=400>
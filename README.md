# Initial setup.
- Python env.
```
pyenv virtualenv 3.6.1 poolmon
```

- Pre-requisites.
```
pip install -r requirements.txt
```

- Initialize app.
```
./manage.py migrate
./manage.py createsuperuser
```

The above should create a sqlite database file and add a super user.
Remember the super user id and password (`admin/detect leak`, e.g.).

- Run app.
```
./manage.py runserver
```

The above starts the server at http://127.0.0.1:8000/.

- Add users.
Login as the super user at http://127.0.0.1:8000/admin.

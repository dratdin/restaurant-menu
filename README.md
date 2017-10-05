# Restaurant menu

Blue services homework

## Carts storage
Carts are stored in db. Access key for each cart is session_key.
It is'n the best approach for storing carts. Because the application neeed to [clear inactive sessions and carts](https://docs.djangoproject.com/en/1.11/topics/http/sessions/#clearing-the-session-store)
And it's also increases the count of db queries. But it's enought for implementing task. I also didn't use the cookie as store for more understanding django, not frontend.

### Install and start
[Create the virtualenv](https://pythontips.com/2013/07/30/what-is-virtualenv/)
```
cd ./to_you_enviroment_folder
```

clone the repository
```
git clone https://github.com/dratdin/restaurant-menu.git
```

```
cd restaurant-menu
```

```
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py loaddata 'categories.json'
python3 manage.py loaddata 'dishes.json'
python3 manage.py runserver
```

After need to run react application 
(In production version of this project python or nginx(it's better) server must return built react application
but in development mode we just run node.js server which work in proxy mode )

```
cd carts-client
npm install
npm start
```

### Enable admin
```
python3 manage.py createsuperuser
```

### Check code coverage
```
coverage run --source='.' --branch manage.py test
coverage report
```

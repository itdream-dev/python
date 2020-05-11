# Setup
* Clone this repo
```
git clone git@bitbucket.org:yoheioka/ivysaur.git
```
* Please use python 2.7 and not python 3
* Create a virtual environment
Consider using [https://virtualenvwrapper.readthedocs.org](virtualenvwrapper) or pyenv to keep things clean.

* Install and run Postgres
[http://postgresapp.com/](Postgres.app) is an easy way to get up and running quick for Mac OSX users. Once you have Postgres installed and running, create a database called `ivysaur` to use as our local development database.
* Set the IVYSAUR_ENV in your shell startup by adding the following. usually ~/.bashrc or ~/.zshrc
```
export IVYSAUR_ENV=development
```

* Install python packages
```
$> pip install -r requirements.txt

note: if you get an error running the above, then try and run the following
sudo PATH=$PATH:/Applications/Postgres.app/Contents/Versions/9.6/bin pip install psycopg2
brew install postgresql
```

* Install python developer packages

Python packages required to run tests and debuging

```
$> pip install -r requirements_dev.txt
```

* Database migrations are handled using [https://flask-migrate.readthedocs.org/en/latest/](Flask-Migrate). You will have to run the following commands.
```
$> python manage.py db upgrade
```
* Initalize the Roles table by running the following
```
$> python manage.py create_roles
```

* You may need to do the following
```
mkdir -p /var/log/ivysaur
sudo touch /var/log/ivysaur/ivysaur.log
sudo chmod 666 /var/log/ivysaur/ivysaur.log
sudo touch /var/log/ivysaur/manage.log
sudo chmod 666 /var/log/ivysaur/manage.log
```

To start the server:
```
$> python ivysaur.py
```

To start the server in DEBUG mode:
```
$> python ivysaur.py --logging=DEBUG
```

Run tests

* Attention. Create test db with name: _test_ivysaur_ to  run tests
```
$> python run_tests.py
```
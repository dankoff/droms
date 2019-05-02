# DROMS
*Distributed Restaurant and Order Management System built in Flask*.

## How to install
Clone the repository
```
git clone https://github.com/dankoff/droms
```
Navigate to the *droms* folder
```
cd droms
```
Create a virtual environment and activate it:
```
# Linux/Mac
python3 -m venv venv
. venv/bin/activate

# Windows
py -3 -m venv venv
venv\Scripts\activate.bat
```
Install DROMS
```
pip install -e .
```

## How to run

While still inside the virtual environment, type:
```
# Linux/Mac
export FLASK_APP=app
export FLASK_ENV=development

# Windows
set FLASK_APP=app
set FLASK_ENV=development
```

Then initialise the database:
```
flask init-db
```

Now you may start the server by typing:
```
flask run
```

If you want to be able to connect with other devices, use this command instead:
```
flask run --host=0.0.0.0
```

The app should now be running, open http://127.0.0.1:5000 in a browser to verify

You will need a manager account to be able to log in - use the following credentials:
```
username: manager
password: 123456
```

## Test

```
pip install pytest coverage
pytest
```

Run with coverage report:
```
coverage run -m pytest
coverage report
```

If you want to see the coverage results in the browser, generate html files instead via:
```
coverage html
```
then open the chosen file inside the htmlcov/ in a browser
